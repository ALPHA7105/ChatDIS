(function () {
    var DEFAULTS = {
        position: 'bottom-right',
        width: '380px',
        height: '600px',
        buttonSize: '60px',
        zIndex: 99999
    };

    var config = window.ChatDISConfig || {};
    var serverUrl = config.serverUrl || '';
    var apiKey = config.apiKey || '';
    var position = config.position || DEFAULTS.position;
    var width = config.width || DEFAULTS.width;
    var height = config.height || DEFAULTS.height;
    var zIndex = config.zIndex || DEFAULTS.zIndex;

    var isOpen = false;

    var toggleBtn = document.createElement('button');
    toggleBtn.id = 'chatdis-toggle';
    toggleBtn.setAttribute('aria-label', 'Open ChatDIS');
    toggleBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:28px;height:28px"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>';

    var btnStyles = [
        'position:fixed',
        'z-index:' + (zIndex + 1),
        'width:' + DEFAULTS.buttonSize,
        'height:' + DEFAULTS.buttonSize,
        'border-radius:50%',
        'border:none',
        'cursor:pointer',
        'display:flex',
        'align-items:center',
        'justify-content:center',
        'background:linear-gradient(135deg, #A0522D 0%, #7A3B1E 100%)',
        'color:#fff',
        'box-shadow:0 4px 20px rgba(160,82,45,0.35), 0 0 0 0 rgba(160,82,45,0.3)',
        'transition:all 0.3s ease',
        'animation:chatdis-btn-pulse 3s ease-in-out infinite'
    ];

    if (position === 'bottom-left') {
        btnStyles.push('bottom:24px', 'left:24px');
    } else {
        btnStyles.push('bottom:24px', 'right:24px');
    }

    toggleBtn.style.cssText = btnStyles.join(';');

    var container = document.createElement('div');
    container.id = 'chatdis-container';

    var containerStyles = [
        'position:fixed',
        'z-index:' + zIndex,
        'width:' + width,
        'height:' + height,
        'max-height:calc(100vh - 100px)',
        'max-width:calc(100vw - 32px)',
        'border-radius:16px',
        'overflow:hidden',
        'box-shadow:0 12px 48px rgba(61,43,31,0.18), 0 2px 8px rgba(0,0,0,0.06)',
        'opacity:0',
        'transform:translateY(20px) scale(0.95)',
        'pointer-events:none',
        'transition:all 0.35s cubic-bezier(0.4, 0, 0.2, 1)',
        'border:1px solid rgba(232,213,183,0.5)'
    ];

    if (position === 'bottom-left') {
        containerStyles.push('bottom:96px', 'left:24px');
    } else {
        containerStyles.push('bottom:96px', 'right:24px');
    }

    container.style.cssText = containerStyles.join(';');

    var widgetUrl = serverUrl + '/widget';
    if (apiKey) {
        widgetUrl += '?key=' + encodeURIComponent(apiKey);
    }

    var iframe = document.createElement('iframe');
    iframe.src = widgetUrl;
    iframe.style.cssText = 'width:100%;height:100%;border:none;';
    iframe.setAttribute('title', 'ChatDIS - Dunes International School Assistant');

    iframe.onload = function () {
        if (apiKey) {
            iframe.contentWindow.CHATDIS_API_KEY = apiKey;
        }
        if (serverUrl) {
            iframe.contentWindow.CHATDIS_API_URL = serverUrl + '/ask';
        }
    };

    container.appendChild(iframe);

    var style = document.createElement('style');
    style.textContent = '@keyframes chatdis-btn-pulse{0%,100%{box-shadow:0 4px 20px rgba(160,82,45,0.35),0 0 0 0 rgba(160,82,45,0.3)}50%{box-shadow:0 4px 20px rgba(160,82,45,0.35),0 0 0 8px rgba(160,82,45,0)}}#chatdis-toggle:hover{transform:scale(1.08);box-shadow:0 6px 24px rgba(160,82,45,0.45)!important}@media(max-width:480px){#chatdis-container{width:100vw!important;height:100vh!important;max-height:100vh!important;max-width:100vw!important;bottom:0!important;right:0!important;left:0!important;border-radius:0!important}}';
    document.head.appendChild(style);

    document.body.appendChild(container);
    document.body.appendChild(toggleBtn);

    toggleBtn.addEventListener('click', function () {
        isOpen = !isOpen;
        if (isOpen) {
            container.style.opacity = '1';
            container.style.transform = 'translateY(0) scale(1)';
            container.style.pointerEvents = 'auto';
            toggleBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:24px;height:24px"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';
            toggleBtn.style.animation = 'none';
        } else {
            container.style.opacity = '0';
            container.style.transform = 'translateY(20px) scale(0.95)';
            container.style.pointerEvents = 'none';
            toggleBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:28px;height:28px"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>';
            toggleBtn.style.animation = 'chatdis-btn-pulse 3s ease-in-out infinite';
        }
    });
})();
