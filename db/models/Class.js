const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const slug = require('mongoose-slug-generator');
const mongooseDelete = require('mongoose-delete');

mongoose.plugin(slug);

const Class = new Schema({
    monhoc: {type: String},
    nhom: {type: Number},
    phonghoc: {type: String},
    giangvien: {type: String},
    siso: {type: Number},
    start:{type: Date},
    end:{type: Date},
},{
    timestamps: true,
});

Class.plugin(mongooseDelete,{
    overrideMethods: 'all',
    deletedAt: true,
})
module.exports = mongoose.model('Class',Class);
