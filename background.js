chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!message.text) return;

  chrome.tts.getVoices((voices) => {
    if (!Array.isArray(voices) || voices.length === 0) {
      console.error("No voices available.");
      return;
    }

    const preferredVoice = voices.find(v => v.name && v.name.includes("Google US English"));
    const voiceToUse = preferredVoice || voices[0];

    chrome.tts.speak(message.text, {
      voiceName: voiceToUse.name,
      rate: 1.0,
      pitch: 1.0,
      volume: 1.0
    });
  });
});
// This script listens for messages from the popup and uses the Chrome TTS API to read the selected text aloud.
// It checks for available voices and uses a preferred voice if available, otherwise defaults to the first voice.