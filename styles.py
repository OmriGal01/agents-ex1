"""Styling constants for Omri's digital career chatbot Gradio app (IDE Dark Grey + Blue theme)."""

CSS = """
:root, body, body:not(.dark), .dark {
  --ide-bg: #1e1f22;
  --ide-surface: #26282c;
  --ide-surface-2: #32353b;
  --ide-input-bg: #26282c;
  --ide-border: #3e4148;
  --ide-border-strong: #52565f;
  --ide-text: #dfe1e5;
  --ide-muted: #9397a1;
  --ide-blue: #3574f0;
  --ide-blue-hover: #4a85f6;
  --ide-blue-bubble: #2959c4;
  --ide-blue-glow: rgba(53, 116, 240, 0.25);
}

footer, .built-with, .show-api, .api-docs {
  display: none !important;
}

/* ---------- Viewport-fitting root layout ---------- */
html, body, gradio-app {
  background: var(--ide-bg) !important;
  color: var(--ide-text) !important;
  height: 100dvh !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}

.gradio-container {
  background: var(--ide-bg) !important;
  color: var(--ide-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  width: 100% !important;
  max-width: min(1080px, 96vw) !important;
  height: 100dvh !important;
  max-height: 100dvh !important;
  margin: 0 auto !important;
  padding: 16px 24px 20px !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
}

.gradio-container > .main,
.gradio-container .contain,
.gradio-container .wrap,
.gradio-container .column:has(.chatbot),
.gradio-container .column:has([data-testid="chatbot"]) {
  display: flex !important;
  flex-direction: column !important;
  flex: 1 1 auto !important;
  min-height: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
  gap: 10px !important;
}

.gradio-container * {
  min-width: 0;
  box-sizing: border-box;
}

/* ---------- Title & Description ---------- */
.gradio-container h1 {
  color: var(--ide-text) !important;
  font-size: 25px !important;
  font-weight: 600 !important;
  letter-spacing: -0.01em !important;
  border-left: 3px solid var(--ide-blue) !important;
  padding-left: 12px !important;
  margin: 0 0 2px !important;
  text-align: left !important;
  flex-shrink: 0 !important;
}

.gradio-container .description,
.gradio-container .markdown p {
  color: var(--ide-muted) !important;
  font-size: 15px !important;
  margin: 0 0 4px !important;
  flex-shrink: 0 !important;
}

/* ---------- Block surfaces (exclude the chatbot box) ---------- */
.block:not(.chatbot):not([data-testid="chatbot"]):not(:has([data-testid="chatbot"])),
.form {
  background: transparent !important;
  box-shadow: none !important;
  border: 0 !important;
}

/* ---------- Hide Chatbot header strip ---------- */
.chatbot > .block-label,
.chatbot > label,
.chatbot .label-wrap,
.chatbot .block-label,
.chatbot > .label-container,
[data-testid="chatbot"] > .label-container,
[data-testid="chatbot"] .block-label {
  display: none !important;
}

/* ---------- Framed / Boxed Chatbot Panel ---------- */
.block:has(> [data-testid="chatbot"]),
.block:has(> .chatbot),
.chatbot,
.chatbot.block,
[data-testid="chatbot"] {
  background: var(--ide-surface) !important;
  border: 1.5px solid var(--ide-border-strong) !important;
  border-radius: 8px !important;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
  flex: 1 1 auto !important;
  height: calc(100dvh - 190px) !important;
  min-height: 420px !important;
  max-height: calc(100dvh - 190px) !important;
  overflow-y: auto !important;
}

/* Avoid double border if both outer .block and inner [data-testid="chatbot"] match */
.block:has(> [data-testid="chatbot"]) > [data-testid="chatbot"],
.block:has(> .chatbot) > .chatbot {
  border: 0 !important;
  box-shadow: none !important;
  height: 100% !important;
  max-height: 100% !important;
}

.chatbot .placeholder,
.chatbot .placeholder *,
[data-testid="chatbot"] .placeholder,
[data-testid="chatbot"] .placeholder * {
  color: var(--ide-muted) !important;
  font-size: 15px !important;
}

/* ---------- Timer / StatusTracker (keep ticking timer, hide ETA bar) ---------- */
.eta-bar {
  display: none !important;
}

.progress-text, .meta-text, .meta-text-center {
  background: var(--ide-surface-2) !important;
  color: var(--ide-blue-hover) !important;
  border: 1px solid var(--ide-border) !important;
  border-radius: 4px !important;
  font-family: 'JetBrains Mono', 'SF Mono', Consolas, monospace !important;
  font-size: 13px !important;
  padding: 3px 9px !important;
}

/* ---------- Message rows & Compact Bubbles ---------- */
.message-row,
.message-row > div,
.message-row .role,
.message-wrap,
.bubble-wrap {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

.message-row {
  margin-top: 4px !important;
  margin-bottom: 4px !important;
}

.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  border: 0 !important;
  border-radius: 6px !important;
  box-shadow: none !important;
  padding: 5px 12px !important;
  min-height: 0 !important;
  font-size: 16px !important;
  line-height: 1.42 !important;
  unicode-bidi: plaintext !important;
  text-align: start !important;
}

/* Strip nested padding so single-line bubbles don't get double vertical padding */
.message-row .message .message,
.message-row .message .bubble,
.message-row .message .message-bubble,
.message-row .bubble .message,
.message-row .bubble .bubble,
.message-row .bubble .message-bubble,
.message-row .message-bubble .message,
.message-row .message-bubble .bubble,
.message-row .message-bubble .message-bubble,
.message-row .prose,
.message-row .md,
.message-row .message-content {
  padding: 0 !important;
  margin: 0 !important;
  min-height: 0 !important;
}

/* ---------- User & Assistant Bubble Colors ---------- */
.message-row.user-row .message,
.message-row.user-row .message-bubble,
.message-row.user-row .bubble,
.message-row[data-role="user"] .message,
.message-row[data-role="user"] .message-bubble {
  background: var(--ide-blue-bubble) !important;
  color: #ffffff !important;
}

.message-row.bot-row .message,
.message-row.bot-row .message-bubble,
.message-row.bot-row .bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .message-bubble {
  background: var(--ide-surface-2) !important;
  color: var(--ide-text) !important;
  border-left: 2px solid var(--ide-blue) !important;
}

/* Prevent duplicate left border on nested elements */
.message-row.bot-row .message .message,
.message-row.bot-row .message .bubble,
.message-row.bot-row .message .message-bubble,
.message-row.bot-row .bubble .message,
.message-row.bot-row .bubble .bubble,
.message-row.bot-row .bubble .message-bubble,
.message-row.bot-row .message-bubble .message,
.message-row.bot-row .message-bubble .bubble,
.message-row.bot-row .message-bubble .message-bubble,
.message-row[data-role="assistant"] .message .message,
.message-row[data-role="assistant"] .message .bubble,
.message-row[data-role="assistant"] .message .message-bubble,
.message-row[data-role="assistant"] .bubble .message,
.message-row[data-role="assistant"] .bubble .bubble,
.message-row[data-role="assistant"] .bubble .message-bubble,
.message-row[data-role="assistant"] .message-bubble .message,
.message-row[data-role="assistant"] .message-bubble .bubble,
.message-row[data-role="assistant"] .message-bubble .message-bubble {
  border-left: 0 !important;
}

/* ---------- Typography inside bubbles ---------- */
.message-row .message p,
.message-row .message-bubble p,
.message-row .bubble p,
.message-row .prose p,
.message-row .message li,
.message-row .message-bubble li,
.message-row .bubble li,
.message-row .prose li {
  font-size: 16px !important;
  line-height: 1.42 !important;
  margin: 0 0 6px !important;
  padding: 0 !important;
  color: inherit !important;
  unicode-bidi: plaintext !important;
  text-align: start !important;
}

.message-row .message p:last-child,
.message-row .message-bubble p:last-child,
.message-row .bubble p:last-child,
.message-row .prose p:last-child {
  margin-bottom: 0 !important;
}

.message-row .message *,
.message-row .message-bubble *,
.message-row .bubble * {
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
  color: inherit !important;
}

.message-row .message a,
.message-row .message-bubble a {
  color: var(--ide-blue-hover) !important;
  text-decoration: underline;
}

/* ---------- Input row ---------- */
.input-row,
.gr-input-row,
.chat-input-row,
form[class*="input"] {
  align-items: stretch !important;
  flex-shrink: 0 !important;
}

textarea, input[type="text"] {
  background: var(--ide-input-bg) !important;
  border: 1.5px solid var(--ide-border-strong) !important;
  border-radius: 6px !important;
  color: var(--ide-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 16px !important;
  padding: 10px 14px !important;
  line-height: 1.4 !important;
  min-height: 46px !important;
  unicode-bidi: plaintext !important;
  text-align: start !important;
}

textarea:focus, input[type="text"]:focus {
  border-color: var(--ide-blue) !important;
  outline: none !important;
  box-shadow: 0 0 0 2px var(--ide-blue-glow) !important;
}

textarea::placeholder, input::placeholder {
  color: var(--ide-muted) !important;
}

/* ---------- Buttons ---------- */
button {
  font-family: 'JetBrains Mono', 'SF Mono', Consolas, monospace !important;
  letter-spacing: 0.06em !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  border: 1px solid var(--ide-border-strong) !important;
  border-radius: 6px !important;
  background: var(--ide-surface) !important;
  color: var(--ide-text) !important;
  padding: 0 16px !important;
  min-height: 46px !important;
  align-self: stretch !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}

button:hover {
  border-color: var(--ide-blue) !important;
  color: var(--ide-blue-hover) !important;
}

button.primary,
button[variant="primary"],
button.submit,
button.submit-button,
.submit-button,
button.lg.primary {
  background: var(--ide-blue) !important;
  border: 1px solid var(--ide-blue) !important;
  color: #ffffff !important;
  min-height: 46px !important;
  align-self: stretch !important;
  padding: 0 16px !important;
}

button.primary:hover,
button.submit:hover,
.submit-button:hover,
button.lg.primary:hover {
  background: var(--ide-blue-hover) !important;
  border-color: var(--ide-blue-hover) !important;
  color: #ffffff !important;
}

button.submit svg,
button.submit-button svg,
.submit-button svg,
button.primary svg,
button[variant="primary"] svg {
  width: 18px !important;
  height: 18px !important;
  margin: 0 auto !important;
  display: block !important;
  align-self: center !important;
  color: #ffffff !important;
  fill: currentColor !important;
  stroke: currentColor !important;
}

/* ---------- Icon buttons (clear, retry, copy) ---------- */
.icon-button, .chatbot .icon-button {
  color: var(--ide-muted) !important;
  background: transparent !important;
  border: 0 !important;
  min-height: 0 !important;
  align-self: auto !important;
  padding: 4px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.icon-button:hover, .chatbot .icon-button:hover {
  color: var(--ide-blue-hover) !important;
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--ide-bg); }
::-webkit-scrollbar-thumb { background: var(--ide-border-strong); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--ide-blue); }

/* ---------- Selection ---------- */
::selection {
  background: var(--ide-blue);
  color: #ffffff;
}

/* ---------- Mobile & small screens ---------- */
@media (max-width: 640px) {
  .gradio-container {
    max-width: 100vw !important;
    padding: 12px 12px 14px !important;
  }
  .gradio-container h1 {
    font-size: 20px !important;
  }
}
"""

JS = """
() => {
  document.title = "Omri's digital career chatbot";
  document.documentElement.classList.add('dark');
  document.body.classList.add('dark');

  const focusInput = () => {
    const areas = document.querySelectorAll('textarea');
    if (areas.length) areas[areas.length - 1].focus();
  };
  setTimeout(focusInput, 300);

  const watchTextarea = (area) => {
    if (area.dataset.watched) return;
    area.dataset.watched = '1';
    area.setAttribute('dir', 'auto');
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
    }).observe(area, { attributes: true, attributeFilter: ['disabled', 'readonly'] });
  };

  const applyAutoDir = () => {
    document
      .querySelectorAll('.message p, .message li, .message ul, .message ol, .prose p, .prose li')
      .forEach((el) => {
        if (!el.getAttribute('dir')) el.setAttribute('dir', 'auto');
      });
  };

  // Strip the static ETA denominator (e.g. "1.2s / 3.4s" -> "1.2s") before paint
  const stripEtaFromTimers = () => {
    document.querySelectorAll('.progress-text').forEach((el) => {
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) {
        if (node.nodeValue && node.nodeValue.includes('/')) {
          const cleaned = node.nodeValue.replace(/\\s*\\/\\s*\\d+(?:\\.\\d+)?s/g, '');
          if (cleaned !== node.nodeValue) {
            node.nodeValue = cleaned;
          }
        }
      }
    });
  };

  const scan = () => {
    document.querySelectorAll('textarea').forEach(watchTextarea);
    applyAutoDir();
    stripEtaFromTimers();
  };
  setTimeout(scan, 300);
  new MutationObserver(scan).observe(document.body, {
    childList: true,
    subtree: true,
    characterData: true,
  });
}
"""
