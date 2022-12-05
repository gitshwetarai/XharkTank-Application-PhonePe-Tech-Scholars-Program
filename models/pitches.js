// Defining Pitch Schema

const mongoose = require("mongoose");
const validator = require("validator");
// const normalize = require ('normalize-mongoose');



const pitchSchema = new mongoose.Schema({

    
    entrepreneur: {
        type: String,
        required: true
    },

    pitchTitle: {
        type: String,
        required: true
    },

    pitchIdea: {
        type: String,
        required: true
    },
    askAmount: {
        type: Number,
        required: true
    },

    equity: {
        type: Number,
        required: true
    },

    offers : [
        {
            id: {type: String},
            investor: {type: String},
            amount: {type: Number},
            equity: {type: Number},
            comment: {type: String},
        }
    ]

    
}, { timestamps: true })

// pitchSchema.plugin(normalize);

// Create collection using model
const Pitch = new mongoose.model('Pitch', pitchSchema);



module.exports = Pitch;

