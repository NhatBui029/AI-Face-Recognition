const { default: mongoose } = require("mongoose")

module.exports = {
    multipleMongooseToObject: (mongooses) => {
        return mongooses.map(mongoose => mongoose.toObject())
    },
    mongooseToObject: (mongoose) => {
        return mongoose ? mongoose.toObject() : mongoose
    },
    formatDate: (date) => {
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const year = date.getFullYear();
        const hours = date.getHours();
        const minutes = date.getMinutes();
        const seconds = date.getSeconds();
        return `${hours}h:${minutes} - ${day}/${month}/${year}`;
    },
}