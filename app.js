var express = require("express");
var path = require("path");
var cookieParser = require("cookie-parser");
var logger = require("morgan");
const mongoose = require("mongoose");
// var mongoose = require("./db");

// var indexRouter = require("./routes/index");
// var usersRouter = require("./routes/users");
const PitchRouter = require("./Routers/pitch");

var app = express();

mongoose
  .connect("mongodb://127.0.0.1:27017/xharktank", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("DB is connected"))
  .catch((err) => console.log(err));

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));

// app.use("/", indexRouter);
// app.use("/users", usersRouter);
app.use(PitchRouter);

module.exports = app;
