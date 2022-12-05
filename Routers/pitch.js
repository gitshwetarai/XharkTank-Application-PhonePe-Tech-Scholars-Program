const express = require("express");
const Pitch = require("../models/pitches");

//create router
const router = new express.Router();

//define router
// 1.
router.post("/pitches", async(req, res) => {

    const user = new Pitch(req.body);

    try{
        
        if(!user)
            res.status(400).send();
        
        if(!req.body['entrepreneur'] || !req.body['pitchTitle'] || !req.body['pitchIdea'] || !parseFloat(req.body['askAmount']) || !parseFloat(req.body['equity']) || parseFloat(req.body['equity']) > 100)
        {
            res.status(400).send();
            return;
        }

        const postPitch = await Pitch.create(user, function(err, getId) {
            if(err) throw err;
            const id = getId._id;

            res.status(201).json({id : id});
            res.end();
        })
    }
    catch(e) {
        res.status(400).json({messege: e.messege});
    }
})

// 2.
router.post("/pitches/:id/makeOffer", async(req, res) => {

    const _id = req.params.id;  //fetch id
    console.log(_id);

    if(!_id)
        res.status(404).send();


    try{

        const findPitch = await Pitch.findById(_id).exec();
        console.log(findPitch);
    
        if(!findPitch)
        {
            res.status(404).send();
            return;
        }
        
        if(!req.body['investor'] || !parseFloat(req.body['amount']) || !parseFloat(req.body['equity']) || !req.body['comment'] || parseFloat(req.body['equity']) > 100)
        {
            res.status(400).send();
            return;
        }

        await Pitch.updateOne({_id}, {$push: {offers: {id: findPitch.offers.length+1, ...req.body}}}).exec();

        res.status(201).json({"id" : findPitch.offers.length+1});
    }
    catch(e) {
        // console.log(e);
        res.status(400).json({messege: e.messege});
    }
})

// 3.
router.get("/pitches", async (req, res)=> {
    try
    {
        let ReadAllData = await Pitch.find().select({createdAt: 0, updatedAt: 0, __v: 0}).sort({createdAt: -1, updatedAt: -1});

        const newAllData = ReadAllData.map((data) => {
            const newData = {
              id: data._id,
              entrepreneur: data.entrepreneur,
              pitchTitle: data.pitchTitle,
              pitchIdea: data.pitchIdea,
              askAmount: data.askAmount,
              equity: data.equity,
              offers: data.offers,
            }
            return newData
          })

        // ReadAllData = ReadAllData.map((data) => {
        //     // console.log(data);
        //     data['id'] = data._id.toString();
        //     delete data._id;
        //     return data;
        // })
        // ReadAllData[0]["id"] = ReadAllData[0]["_id"];
        // delete ReadAllData[0]._id;

        // let oneEle = {... ReadAllData[0]._doc};
        // oneEle["id"] = oneEle._id;
        // delete oneEle._id
        // console.log(oneEle)
        console.log(newAllData);
        res.status(200).send(newAllData);
    }
    catch(e) {
        res.send(e);
    }
})

// 4.
router.get("/pitches/:id", async (req, res) => {

    const _id = req.params.id;  //fetch id

    if(!_id)
        res.status(404).send();

    // console.log(_id);
    try{
        const readOneData = await Pitch.findById(_id).exec();
        // console.log(readOneData);

        if(!readOneData)
            res.status(404).send();
        
        else
        {
            const resbody = {id : readOneData._doc._id, entrepreneur: readOneData._doc.entrepreneur, pitchTitle: readOneData._doc.pitchTitle, pitchIdea: readOneData._doc.pitchIdea, askAmount: readOneData._doc.askAmount , equity: readOneData._doc.equity, offers: readOneData._doc.offers}
            res.status(200).send(resbody);
        }

    }
    catch(e) {
        res.status(404).json({messege: e.messege});  
    }
})

module.exports = router;