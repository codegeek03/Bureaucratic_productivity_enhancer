require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');

const app = express();
const saltRounds = 10;

// Middleware
app.use(cors());
app.use(bodyParser.json());

function getCurrentUTCDateTime() {
    const now = new Date();
    return now.toISOString().replace('T', ' ').slice(0, 19);
}

mongo_uri = process.env.MONGODB_URI;
if (!mongo_uri) {
    console.error('MongoDB URI missing');
    process.exit(1);
}
// MongoDB Connection
mongoose.connect(mongo_uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('MongoDB connection error:', err));

// User Schema
const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
        trim: true
    },
    username: {
        type: String,
        required: true,
        unique: true,
        trim: true
    },
    email: {
        type: String,
        required: true,
        unique: true,
        trim: true,
        lowercase: true
    },
    phone: {
        type: String,
        required: true,
    },
    password: {
        type: String,
        required: true
    },
    workExperience: {
        type: String,
        required: true,
    },
    designation: {
        type: String,
        required: true,
        trim: true
    },
    age: {
        type: Number,
        required: true,
        min: 18,
        max: 100
    },
    registrationDateTime: {
        type: String,
        required: true
    },
    registeredBy: {
        type: String,
        required: true,
        default: 'bibhabasuiitkgp'
    }
});

// User Model
const User = mongoose.model('User', userSchema);

// Register Route
app.post('/api/register', async (req, res) => {
    console.log(req.body);
    try {
        const {
            name,
            username,
            email,
            phone,
            password,
            experience,
            designation,
            age
        } = req.body;

        // Hash password
        const hashedPassword = await bcrypt.hash(password, saltRounds);

        // Create new user
        const user = new User({
            name,
            username,
            email,
            phone,
            password: hashedPassword,
            workExperience: experience,
            designation,
            age,
            registrationDateTime: getCurrentUTCDateTime(),
            registeredBy: 'bibhabasuiitkgp'
        });

        const savedUser = await user.save();

        res.status(201).json({
            success: true,
            user: {
                name: savedUser.name,
                username: savedUser.username,
                email: savedUser.email,
                phone: savedUser.phone,
                designation: savedUser.designation,
                experience: savedUser.workExperience,
                age: savedUser.age,
                registrationDateTime: savedUser.registrationDateTime
            }
        });
    } catch (error) {
        if (error.code === 11000) {
            res.status(400).json({
                success: false,
                message: 'Username or email already exists'
            });
        } else {
            res.status(500).json({
                success: false,
                message: 'Error registering user',
                error: error.message
            });
        }
    }
});

// Login Route
app.post('/api/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        // Find user and explicitly include password
        const user = await User.findOne({ username }).select('+password');

        if (!user) {
            return res.status(401).json({
                success: false,
                message: 'Invalid username or password'
            });
        }

        // Compare passwords
        const isMatch = await bcrypt.compare(password, user.password);

        if (!isMatch) {
            return res.status(401).json({
                success: false,
                message: 'Invalid username or password'
            });
        }

        // Send user data (excluding password)
        const userData = {
            name: user.name,
            username: user.username,
            email: user.email,
            phone: user.phone,
            designation: user.designation,
            experience: user.workExperience,
            age: user.age,
            registrationDateTime: user.registrationDateTime
        };

        res.json({
            success: true,
            user: userData
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error during login',
            error: error.message
        });
    }
});
app.get('/', (req, res) => { res.send('Welcome to Startup API'); });
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});