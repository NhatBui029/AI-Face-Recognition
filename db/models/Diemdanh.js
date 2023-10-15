const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const slug = require('mongoose-slug-generator');
const mongooseDelete = require('mongoose-delete');

mongoose.plugin(slug);

const Diemdanh = new Schema({
    ten: {type: String},
    lop: {type: String},
    thoigian:{type: String},
},{
    timestamps: true,
});

Diemdanh.plugin(mongooseDelete,{
    overrideMethods: 'all',
    deletedAt: true,
})
module.exports = mongoose.model('Diemdanh',Diemdanh);
