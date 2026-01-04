const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const cors = require('cors');

const app = express();
const PORT = 3000;

// Configurar middleware
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

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

// Rota para adicionar produto
app.post('/api/add-product', upload.single('image'), (req, res) => {
    try {
        const { category, subcategory, productName } = req.body;

        if (!category || !productName || !req.file) {
            return res.status(400).json({ error: 'Todos os campos são obrigatórios' });
        }

        const imagePath = req.file.path.replace(__dirname + path.sep, '');

        res.json({
            success: true,
            message: `Produto "${productName}" adicionado com sucesso!`,
            imagePath: imagePath.replace(/\\/g, '/')
        });
    } catch (error) {
        console.error('Erro ao adicionar produto:', error);
        res.status(500).json({ error: 'Erro ao adicionar produto: ' + error.message });
    }
});

// Rota para regerar o HTML
app.post('/api/regenerate-html', (req, res) => {
    try {
        const { exec } = require('child_process');

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