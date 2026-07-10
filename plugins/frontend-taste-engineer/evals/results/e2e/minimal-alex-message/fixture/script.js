const replayButton = document.querySelector(".replay");
const replayStatus = document.querySelector("#replay-status");
const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");

let replayTimer;

replayButton?.addEventListener("click", () => {
  window.clearTimeout(replayTimer);

  if (motionPreference.matches) {
    replayStatus.textContent = "The full message is shown.";
    return;
  }

  document.body.classList.remove("is-replaying");
  void document.body.offsetWidth;
  document.body.classList.add("is-replaying");
  replayButton.disabled = true;
  replayStatus.textContent = "Replaying the message.";

  replayTimer = window.setTimeout(() => {
    document.body.classList.remove("is-replaying");
    replayButton.disabled = false;
    replayStatus.textContent = "The message is ready again.";
    replayButton.focus();
  }, 1550);
});
