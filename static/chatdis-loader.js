(function () {
    var DEFAULTS = {
        position: 'bottom-right',
        width: '380px',
        height: '600px',
        buttonSize: '65px', // Slightly larger for better visibility
        zIndex: 99999
    };

    var config = window.ChatDISConfig || {};
    var serverUrl = config.serverUrl || '';
    var position = config.position || DEFAULTS.position;
    var width = config.width || DEFAULTS.width;
    var height = config.height || DEFAULTS.height;
    var zIndex = config.zIndex || DEFAULTS.zIndex;

    var isOpen = false;

    // 1. Create the Welcome Tooltip
    var tooltip = document.createElement('div');
    tooltip.id = 'chatdis-tooltip';
    tooltip.innerHTML = 'Hi, I am <strong>ChatDIS</strong>! <br>How can I help?';
    
    // 2. Define Logo HTML
    var logoHtml = '<img src="' + serverUrl + '/static/duneslogo.png" alt="DIS Logo" style="width:100%; height:100%; aspect-ratio: 1 / 1; border-radius:50%; object-fit:cover; display:block; border: 2px solid #C9953A; flex-shrink: 0;">';   //var logoHtml = '<img src="' + serverUrl + '/static/duneslogo.png" alt="DIS Logo" style="width:100%; height:100%; aspect-ratio: 1/1; border-radius:50%; object-fit:cover; display:block; border: 2px solid #C9953A; min-width: 100%;">';

    // 3. Create Toggle Button
    var toggleBtn = document.createElement('button');
    toggleBtn.id = 'chatdis-toggle';
    toggleBtn.innerHTML = logoHtml;

    // Apply Button Styles (Moving most to the <style> block for cleaner code)
    var btnPosition = (position === 'bottom-left') ? 'bottom:24px; left:24px;' : 'bottom:24px; right:24px;';
    toggleBtn.style.cssText = btnPosition + 'position:fixed; z-index:' + (zIndex + 1) + '; width:' + DEFAULTS.buttonSize + '; height:' + DEFAULTS.buttonSize + '; border-radius:50%; border:none; cursor:pointer; background:#fff; box-shadow:0 8px 24px rgba(0,0,0,0.2); display:flex; align-items:center; justify-content:center; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);';

    // 4. Create the Container (The Chat Window)
    var container = document.createElement('div');
    container.id = 'chatdis-container';
    var contPos = (position === 'bottom-left') ? 'bottom:100px; left:24px;' : 'bottom:100px; right:24px;';
    container.style.cssText = contPos + 'position:fixed; z-index:' + zIndex + '; width:' + width + '; height:' + height + '; max-height:calc(100vh - 150px); max-width:calc(100vw - 40px); border-radius:20px; overflow:hidden; box-shadow:0 15px 50px rgba(0,0,0,0.2); opacity:0; visibility:hidden; transform: translateY(30px) scale(0.9); transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); border:1px solid #E8D5B7;';

    var iframe = document.createElement('iframe');
    iframe.src = serverUrl + '/widget';
    iframe.style.cssText = 'width:100%; height:100%; border:none;';
    container.appendChild(iframe);

    /*
    // 5. Add Advanced CSS Animations & Fonts
    var style = document.createElement('style');
    style.textContent = `
        @import url('https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Syne:wght@400;500;600&display=swap');
    
        #chatdis-tooltip {
            white-space: nowrap !important;
            width: auto !important;
            min-width: fit-content !important;
            box-sizing: border-box !important;
            all: initial;
            position: fixed;
            ${position === 'bottom-left' ? 'left:100px;' : 'right:100px;'}
            bottom: 35px;
            background: #860404;
            color: #FBF7F1;
            padding: 12px 18px;
            border-radius: 12px;
            

            font-family: 'Syne', sans-serif;
            font-weight: 500; 
            font-size: 14px;
            line-height: 1.4;
            
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            z-index: ${zIndex + 1};
            animation: chatdis-fade-in 1s ease 1s both;
            border-left: 4px solid #C9953A;
            pointer-events: none;
        }
    
        #chatdis-tooltip strong {
            font-family: 'Cormorant', serif;
            font-weight: 700;
            font-size: 16px;
            letter-spacing: 0.5px;
        }
    
        #chatdis-tooltip::after {
            content: '';
            position: absolute;
            ${position === 'bottom-left' ? 'left: -8px;' : 'right: -8px;'}
            top: 50%;
            transform: translateY(-50%);
            border-top: 8px solid transparent;
            border-bottom: 8px solid transparent;
            ${position === 'bottom-left' ? 'border-right: 8px solid #860404;' : 'border-left: 8px solid #860404;'}
        } 
    
        @keyframes chatdis-fade-in {
            from { opacity: 0; transform: translateX(${position === 'bottom-left' ? '-10px' : '10px'}); }
            to { opacity: 1; transform: translateX(0); }
        }
    
        #chatdis-toggle {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            aspect-ratio: 1 / 1 !important;
            overflow: hidden !important;
            padding: 0 !important;
        }
        #chatdis-toggle:hover { transform: scale(1.1) rotate(5deg); }
        #chatdis-toggle:active { transform: scale(0.9); }
    `;

    */
    // 5. Add Advanced CSS Animations
    var style = document.createElement('style');
    style.textContent = `
        @import url('https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Syne:wght@400;500;600&display=swap');
        #chatdis-tooltip {
            white-space: nowrap; !important;
            width:auto; !important;
            min-width: fit-content !important;
            box-sizing: content-box !important;
            all: initial;
            position: fixed;
            ${position === 'bottom-left' ? 'left:100px;' : 'right:100px;'}
            bottom: 35px;
            background: #860404;
            color: #FBF7F1;
            padding: 10px 15px;
            border-radius: 12px;
            font-family: 'Syne', sans-serif;
            font-size: 13px;
            box-shadow: 0 5px 15px rgba(201,149,58);
            z-index: ${zIndex + 1};
            animation: chatdis-fade-in 1s ease 1s both;
            border-left: 4px solid #C9953A;
            pointer-events: none;
        }
        #chatdis-tooltip::after {
            content: '';
            position: absolute;
            ${position === 'bottom-left' ? 'left: -8px;' : 'right: -8px;'}
            top: 50%;
            transform: translateY(-50%);
            border-top: 8px solid transparent;
            border-bottom: 8px solid transparent;
            ${position === 'bottom-left' ? 'border-right: 8px solid #C9953A;' : 'border-left: 8px solid #C9953A;'}
        } 
        @keyframes chatdis-fade-in {
            from { opacity: 0; transform: translateX(${position === 'bottom-left' ? '-10px' : '10px'}); }
            to { opacity: 1; transform: translateX(0); }
        }
        #chatdis-toggle {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            aspect-ratio: 1 / 1 !important;
            overflow: hidden !important;
            padding: 0 !important;
        }
        #chatdis-toggle:hover { transform: scale(1.1) rotate(5deg); }
        #chatdis-toggle:active { transform: scale(0.9); }
    `;

    
    
    document.head.appendChild(style);
    document.body.appendChild(container);
    document.body.appendChild(toggleBtn);
    document.body.appendChild(tooltip);

    // 6. Interaction Logic
    toggleBtn.addEventListener('click', function () {
        isOpen = !isOpen;
        if (isOpen) {
            container.style.opacity = '1';
            container.style.visibility = 'visible';
            container.style.transform = 'translateY(0) scale(1)';
            tooltip.style.display = 'none'; // Hide tooltip when chat opens
            toggleBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="#94030f" stroke-width="3" style="width:28px; height:28px"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';
        } else {
            container.style.opacity = '0';
            container.style.visibility = 'hidden';
            container.style.transform = 'translateY(30px) scale(0.9)';
            toggleBtn.innerHTML = logoHtml;
        }
    });
})();




/*
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

    // Define the circular logo HTML
    var logoHtml = '<img src="' + serverUrl + '/static/duneslogo.png" alt="DIS Logo" style="width:100%; height:100%; border-radius:50%; object-fit:cover; display:block;">';

    var toggleBtn = document.createElement('button');
    toggleBtn.id = 'chatdis-toggle';
    toggleBtn.setAttribute('aria-label', 'Open ChatDIS');
    toggleBtn.innerHTML = logoHtml;

    var btnStyles = [
        'position:fixed',
        'z-index:' + (zIndex + 1),
        'width:' + DEFAULTS.buttonSize,
        'height:' + DEFAULTS.buttonSize,
        'padding:4px',
        'border-radius:50%',
        'border:none',
        'cursor:pointer',
        'display:flex',
        'align-items:center',
        'justify-content:center',
        'background:linear-gradient(135deg, #94030f 0%, #690b13 100%)',
        'color:#fff',
        'box-shadow:0 4px 20px rgba(160,82,45,0.35)',
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
        'max-height:calc(100vh - 180px)',
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
        if (apiKey) { iframe.contentWindow.CHATDIS_API_KEY = apiKey; }
        if (serverUrl) { iframe.contentWindow.CHATDIS_API_URL = serverUrl + '/ask'; }
    };

    container.appendChild(iframe);

    var style = document.createElement('style');
    style.textContent = '@keyframes chatdis-btn-pulse{0%,100%{box-shadow:0 4px 20px rgba(148,3,15,0.35),0 0 0 0 rgba(148,3,15,0.3)}50%{box-shadow:0 4px 20px rgba(148,3,15,0.35),0 0 0 8px rgba(148,3,15,0)}} #chatdis-toggle:hover{transform:scale(1.08);box-shadow:0 6px 24px rgba(148,3,15,0.45)!important}';
    document.head.appendChild(style);

    document.body.appendChild(container);
    document.body.appendChild(toggleBtn);

    toggleBtn.addEventListener('click', function () {
        isOpen = !isOpen;
        if (isOpen) {
            container.style.opacity = '1';
            container.style.transform = 'translateY(0) scale(1)';
            container.style.pointerEvents = 'auto';
            // Close icon
            toggleBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:24px;height:24px"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';
            toggleBtn.style.animation = 'none';
        } else {
            container.style.opacity = '0';
            container.style.transform = 'translateY(20px) scale(0.95)';
            container.style.pointerEvents = 'none';
            // Restore Logo
            toggleBtn.innerHTML = logoHtml;
            toggleBtn.style.animation = 'chatdis-btn-pulse 3s ease-in-out infinite';
        }
    });
})();
*/
