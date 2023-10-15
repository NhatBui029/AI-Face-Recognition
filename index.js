const express = require('express')
const app = express()
const morgan = require('morgan')
const handlebars = require('express-handlebars')
const path = require('path')
const db = require('./db/index')
const cookieParser = require('cookie-parser')
const Class = require('./db/models/Class')
const Diemdanh = require('./db/models/Diemdanh')
const util = require('./public/util/mongoose')
const { spawn } = require('child_process')
app.engine(
    'hbs',
    handlebars.engine({
        extname: '.hbs',
        helpers: {
            formatDate: (date) => util.formatDate(date),
        }
    }),
);

app.set('view engine', 'hbs');
app.set('views', path.join(__dirname, 'resources', 'views'));

app.use(
    express.urlencoded({
        extended: true,
    }),
    express.json(),
    morgan('dev'),
    cookieParser(),
    express.static(path.join(__dirname, 'public'))
);

db.connect()

app.get('/giangvien', function (req, res, next) {
    Class.find({})
        .then((classes) => {
            res.render('home', {
                layout: 'main',
                classes: util.multipleMongooseToObject(classes)
            })
        })
        .catch(next)
})

app.get('/sinhvien', function (req, res, next) {
    Class.find({})
        .then((classes) => {
            res.render('diemDanh', {
                layout: 'main',
                classes: util.multipleMongooseToObject(classes)
            })
        })
        .catch(next)
})

app.get('/addClass', (req, res, next) => {
    res.render('addClass', { layout: 'main' })
})


app.post('/addClass', (req, res, next) => {
    const { monhoc, nhom, phonghoc, giangvien, start, end } = req.body;
    const lop = new Class({
        monhoc: monhoc,
        nhom: nhom,
        phonghoc: phonghoc,
        giangvien: giangvien,
        siso: 0,
        start: start,
        end: end
    });

    lop.save()
        .then(() => res.redirect('/giangvien'))
        .catch(next)
})

app.get('/addSinhVien/:id', (req, res, next) => {
    res.render('addSinhVien', {
        layout: 'main',
        id: req.params.id
    })
})

const executePython = async (script, args) => {
    const arguments = args.map(arg => arg.toString());
    const py = spawn('python', [script, ...arguments]);

    const result = await new Promise((resolve, reject) => {
        let output;

        py.stdout.on('data', (data) => {
            output = data.toString();
        })

        py.stderr.on('data', (data) => {
            console.error(`python error occured: ${data}`);
            reject(`error occured: ${script}`);
        })

        py.on('exit', (code) => {
            console.log(`child process exit with code ${code}`);
            resolve(output)
        })
    })
    return result;
}

app.post('/addSinhVien/:id', async (req, res, next) => {
    try {
        const result = await executePython('01_face_dataset.py', [req.body.id, req.body.name]);
        Class.findOne({ _id: req.params.id })
            .then((lop) => {
                Class.updateOne({ _id: req.params.id }, { siso: lop.siso + 1 })
                    .then(() => {
                        res.render('addSvSuccess', {
                            layout: 'main',
                            thongbao: result
                        })
                    })
                    .catch(next)
            })
            .catch(next)

    } catch (error) {
        res.status(500).json({ error: error });
    }
})

app.get('/diemDanh/:id', async (req, res, next) => {
    try {
        const result = await executePython('03_face_recognition.py', [1]);
        if(result !== " "){
            Class.findOne({ _id: req.params.id })
            .then((lop) => {
                let tmp = "Đúng giờ";
                const dihoc = Date.now() - lop.start;
                const bohoc = Date.now() - lop.end;

                if(bohoc > 0) tmp = "Bỏ học"
                else if(dihoc > 0 ) tmp = `Muộn ${Math.round(dihoc / (1000 * 60))} phút`;

                const diemdanh = new Diemdanh({
                    ten: result.replace("\n", ""),
                    lop: req.params.id,
                    thoigian: tmp
                })
                diemdanh.save();
            })
            .catch(next)
        }     
        res.redirect('/sinhvien')
    } catch (error) {
        res.status(500).json({ error: error });
    }
});


app.get('/danhsach/:id', (req, res, next) => {
    Diemdanh.find({ lop: req.params.id })
        .then((diemdanhs) => {
            res.render('danhSach',{
                layout: 'main',
                diemdanhs: util.multipleMongooseToObject(diemdanhs)
            })
        })
        .catch(next)
})

app.listen(3000)