let audioContext;
let oscillator;
let isPlaying = false;

function initAudio() {
  audioContext = new (window.AudioContext || window.webkitAudioContext)();
  oscillator = audioContext.createOscillator();
  oscillator.type = 'sine';
  oscillator.frequency.setValueAtTime(440, audioContext.currentTime); // 440 Hz (A4 note)
  oscillator.start();
  oscillator.disconnect(); // Start disconnected
}

function toggleSound() {
  if (!audioContext) {
    initAudio();
  }

  if (isPlaying) {
    oscillator.disconnect();
    isPlaying = false;
  } else {
    oscillator.connect(audioContext.destination);
    isPlaying = true;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const playButton = document.getElementById('play-sound');
  playButton.addEventListener('click', toggleSound);
});
