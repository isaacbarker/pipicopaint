// define variables for runtime
const canvasInput = document.getElementById("canvas-input");

// resize canvasInput based on screen size
if (window.innerWidth <= 512) {
    canvasInput.width = window.innerWidth * 0.95;
    canvasInput.height = canvasInput.width * (64 / 128);
}

const ctxInput = canvasInput.getContext("2d");

const canvasOutput = document.getElementById("canvas-output")
const ctxOutput = canvasOutput.getContext("2d")

const clearBtn = document.getElementById("clear");
const invertBtn = document.getElementById("invert")
const printBtn = document.getElementById("print")

const penSize1 = document.getElementById("pen-size-1")
const penSize2 = document.getElementById("pen-size-2")
const penSize3 = document.getElementById("pen-size-3")

const canvasOffsetX = canvasInput.offsetLeft;
const canvasOffsetY = canvasInput.offsetTop;

let isDrawing = false;
let isInverted = false;
let penWeight = 5

// canvas functions
const getPosition = (e) => {
    if (e.touches && e.touches.length > 0) {
        return {
            x: e.touches[0].clientX - canvasOffsetX,
            y: e.touches[0].clientY - canvasOffsetY
        };
    } else {
        return {
            x: e.clientX - canvasOffsetX,
            y: e.clientY - canvasOffsetY
        }
    }
};

const draw = (e) => {
    if (!isDrawing) {
        return;
    }

    // draw line to current position
    ctxInput.lineWidth = penWeight;
    ctxInput.lineCap = 'round';
    ctxInput.strokeStyle = 'white';

    const { x, y } = getPosition(e)

    ctxInput.lineTo(x, y);
    ctxInput.stroke();
    ctxOutput.drawImage(canvasInput, 0, 0, canvasInput.width, canvasInput.height, 
        0, 0, canvasOutput.width, canvasOutput.height
    );
};

const clear = () => {
    // set bg as black as initial conditions
    ctxInput.fillStyle = 'black';
    ctxInput.fillRect(0, 0, canvasInput.width, canvasInput.height);
    ctxOutput.drawImage(canvasInput, 0, 0, canvasInput.width, canvasInput.height, 
        0, 0, canvasOutput.width, canvasOutput.height
    );
};

const invert = () => {
    // invert image
    if (isInverted) {
        ctxInput.filter = "invert(0%)";
    } else {
        ctxInput.filter = "invert(100%)";
    }

    clear()
    isInverted = !isInverted;
};

const setWeight = (weight) => {
    penWeight = weight

    if (weight == 3) {
        penSize1.classList.add("selected")
        penSize2.classList.remove("selected")
        penSize3.classList.remove("selected")
    } else if (weight == 5) {
        penSize1.classList.remove("selected")
        penSize2.classList.add("selected")
        penSize3.classList.remove("selected")
    } else if (weight == 9) {
        penSize1.classList.remove("selected")
        penSize2.classList.remove("selected")
        penSize3.classList.add("selected")
    }
}

const start = (e) => {
    // begin path tracking
    e.preventDefault();
    isDrawing = true;
};

const end = (e) => {
    // end path tracking and cut path
    e.preventDefault();
    isDrawing = false;
    ctxInput.stroke();
    ctxInput.beginPath();
};

const print = (e) => {
    let output = ctxOutput.getImageData(0, 0, canvasOutput.width, canvasOutput.height).data
    // decide whether pixel is black or white
    let colourValues = []

    for (let i = 0; i < output.length; i+= 4) {
        colourValues.push(
            Math.round((output[i] + output[i+1] + output[i+2]) / 3 / 255)
        )
    }

    // convert to base 64 bit string
    const byteArray = new Uint8Array(128 * 64 / 8)

    for (let i = 0; i < colourValues.length; i++) {
        const byteIndex = Math.floor(i / 8)
        const bitOffset = 7 - (i % 8);

        if (colourValues[i]) {
            byteArray[byteIndex] |= (1 << bitOffset)
        }
    }

    // push data
    fetch("/", {
        method: "POST",
        body: byteArray,
        headers: {
            "Content-type": "application/octet-stream"
        }
    })
}

// register runtime events and set initial conditions
clear();

clearBtn.addEventListener("click", clear);

invertBtn.addEventListener("click", invert);

printBtn.addEventListener("click", print)

penSize1.addEventListener("click", () => setWeight(3))
penSize2.addEventListener("click", () => setWeight(5))
penSize3.addEventListener("click", () => setWeight(9))

canvasInput.addEventListener("mousedown", start);
canvasInput.addEventListener("touchstart", start);

canvasInput.addEventListener("mouseup", end);
canvasInput.addEventListener("touchend", end);

canvasInput.addEventListener("mousemove", draw);
canvasInput.addEventListener("touchmove", draw);