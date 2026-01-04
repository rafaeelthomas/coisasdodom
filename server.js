const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const cors = require('cors');
const { exec } = require('child_process');
const sharp = require('sharp');

const app = express();

// Configurar middleware
app.use(cors());
app.use(express.json());

// Servir arquivos estáticos com opções para lidar com encoding
app.use(express.static(__dirname, {
    setHeaders: (res, path) => {
        // Garantir encoding correto para caracteres especiais
        if (path.endsWith('.jpg') || path.endsWith('.png') || path.endsWith('.gif') || path.endsWith('.webp')) {
            res.set('Content-Type', 'image/jpeg');
        }
    }
}));

// Configurar multer para upload de imagens
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        const category = req.body.category;
        const subcategory = req.body.subcategory;

        let folderPath = path.join(__dirname, category);
        if (subcategory) {
            folderPath = path.join(folderPath, subcategory);
        }

        // Criar pasta se não existir
        if (!fs.existsSync(folderPath)) {
            fs.mkdirSync(folderPath, { recursive: true });
        }

        cb(null, folderPath);
    },
    filename: function (req, file, cb) {
        const productName = req.body.productName;
        const extension = path.extname(file.originalname);
        cb(null, `${productName}${extension}`);
    }
});

const upload = multer({
    storage: storage,
    limits: {
        fileSize: 5 * 1024 * 1024 // 5MB
    },
    fileFilter: function (req, file, cb) {
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
        if (allowedTypes.includes(file.mimetype)) {
            cb(null, true);
        } else {
            cb(new Error('Tipo de arquivo inválido. Use JPG, PNG, GIF ou WEBP.'));
        }
    }
});

// Rota para criar categoria/subcategoria
app.post('/api/create-category', (req, res) => {
    try {
        const { categoryName, subcategoryName } = req.body;

        if (!categoryName) {
            return res.status(400).json({ error: 'Nome da categoria é obrigatório' });
        }

        let folderPath = path.join(__dirname, categoryName);
        if (subcategoryName) {
            folderPath = path.join(folderPath, subcategoryName);
        }

        // Criar pasta
        if (!fs.existsSync(folderPath)) {
            fs.mkdirSync(folderPath, { recursive: true });
            res.json({
                success: true,
                message: `Categoria "${categoryName}"${subcategoryName ? ' / "' + subcategoryName + '"' : ''} criada com sucesso!`,
                path: folderPath
            });
        } else {
            res.status(400).json({ error: 'Essa categoria já existe!' });
        }
    } catch (error) {
        console.error('Erro ao criar categoria:', error);
        res.status(500).json({ error: 'Erro ao criar categoria: ' + error.message });
    }
});

// Função para gerar thumbnail
async function generateThumbnail(imagePath) {
    try {
        const thumbnailDir = path.join(__dirname, '.thumbnails');
        const imageRelativePath = imagePath.replace(__dirname + path.sep, '');
        const thumbnailPath = path.join(thumbnailDir, imageRelativePath);
        const thumbnailFolder = path.dirname(thumbnailPath);

        // Criar diretório do thumbnail se não existir
        if (!fs.existsSync(thumbnailFolder)) {
            fs.mkdirSync(thumbnailFolder, { recursive: true });
        }

        // Gerar thumbnail com sharp (400x400px)
        await sharp(imagePath)
            .resize(400, 400, {
                fit: 'cover',
                position: 'center'
            })
            .jpeg({ quality: 85 })
            .toFile(thumbnailPath);

        console.log(`✅ Thumbnail gerado: ${thumbnailPath}`);
        return true;
    } catch (error) {
        console.error('❌ Erro ao gerar thumbnail:', error);
        return false;
    }
}

// Rota para adicionar produto
app.post('/api/add-product', upload.single('image'), async (req, res) => {
    try {
        const { category, subcategory, productName } = req.body;

        if (!category || !productName || !req.file) {
            return res.status(400).json({ error: 'Todos os campos são obrigatórios' });
        }

        const imagePath = req.file.path.replace(__dirname + path.sep, '');

        // Gerar thumbnail
        await generateThumbnail(req.file.path);

        // Regenerar HTML automaticamente
        exec(`cd "${__dirname}" && python3 generate_catalog.py`, (error, stdout, stderr) => {
            if (error) {
                console.error('❌ Erro ao regerar HTML:', error);
            } else {
                console.log('✅ HTML regenerado automaticamente');
            }
        });

        res.json({
            success: true,
            message: `Produto "${productName}" adicionado com sucesso!`,
            imagePath: imagePath.replace(/\\/g, '/'),
            needsReload: true
        });
    } catch (error) {
        console.error('Erro ao adicionar produto:', error);
        res.status(500).json({ error: 'Erro ao adicionar produto: ' + error.message });
    }
});

// Rota para deletar produto
app.delete('/api/delete-product', (req, res) => {
    try {
        const { imagePath } = req.body;

        if (!imagePath) {
            return res.status(400).json({ error: 'Caminho da imagem é obrigatório' });
        }

        const fullPath = path.join(__dirname, imagePath);
        const thumbnailPath = path.join(__dirname, '.thumbnails', imagePath);

        // Verificar se o arquivo existe
        if (!fs.existsSync(fullPath)) {
            return res.status(404).json({ error: 'Arquivo não encontrado' });
        }

        // Deletar a imagem original
        fs.unlinkSync(fullPath);
        console.log(`✅ Imagem deletada: ${fullPath}`);

        // Deletar o thumbnail se existir
        if (fs.existsSync(thumbnailPath)) {
            fs.unlinkSync(thumbnailPath);
            console.log(`✅ Thumbnail deletado: ${thumbnailPath}`);
        }

        // Regenerar HTML automaticamente
        exec(`cd "${__dirname}" && python3 generate_catalog.py`, (error, stdout, stderr) => {
            if (error) {
                console.error('❌ Erro ao regerar HTML:', error);
            } else {
                console.log('✅ HTML regenerado após exclusão');
            }
        });

        res.json({
            success: true,
            message: 'Produto deletado com sucesso!',
            needsReload: true
        });
    } catch (error) {
        console.error('Erro ao deletar produto:', error);
        res.status(500).json({ error: 'Erro ao deletar produto: ' + error.message });
    }
});

// Rota para servir imagens com tratamento de encoding
app.get('*.(jpg|jpeg|png|gif|webp)', (req, res, next) => {
    // Decodificar o caminho da URL
    const decodedPath = decodeURIComponent(req.path);
    const filePath = path.join(__dirname, decodedPath);

    // Verificar se o arquivo existe
    if (fs.existsSync(filePath)) {
        res.sendFile(filePath);
    } else {
        next(); // Se não encontrar, deixa o express.static tentar
    }
});

// Rota para regerar o HTML
app.post('/api/regenerate-html', (req, res) => {
    try {
        // Executar o script Python para regerar o HTML
        exec(`cd "${__dirname}" && python3 generate_catalog.py`, (error, stdout, stderr) => {
            if (error) {
                console.error('Erro ao regerar HTML:', error);
                return res.status(500).json({ error: 'Erro ao regerar HTML: ' + error.message });
            }

            res.json({
                success: true,
                message: 'Catálogo atualizado com sucesso! Recarregue a página.',
                output: stdout
            });
        });
    } catch (error) {
        console.error('Erro ao regerar HTML:', error);
        res.status(500).json({ error: 'Erro ao regerar HTML: ' + error.message });
    }
});

// Iniciar servidor

const PORT = process.env.PORT || 3000;

app.listen(PORT, '0.0.0.0', () => {
    console.log(`? Servidor rodando na porta ${PORT}`);
    console.log(`? Diret�rio: ${__dirname}`);
    console.log(`? Acesse: ${process.env.RENDER_EXTERNAL_URL || 'http://localhost:' + PORT}`);
});