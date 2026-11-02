// Лайки на странице медиа-элемента.
// Заменяет Vue-компонент: тот же контракт /api/like/ и тот же UX,
// но без CDN-фреймворка и без инлайн-скрипта с подстановками из шаблона.

const csrfToken = () => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.content : '';
};

export async function postJson(url, payload) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken(),
        },
        credentials: 'same-origin',
        body: JSON.stringify(payload),
    });
    let data = {};
    try {
        data = await response.json();
    } catch (error) {
        data = { success: false, error: 'invalid JSON response' };
    }
    return { ok: response.ok, data };
}

function initLikeWidget() {
    const widget = document.querySelector('[data-like-widget]');
    if (!widget) {
        return;
    }

    const button = widget.querySelector('[data-like-button]');
    const icon = widget.querySelector('[data-like-icon]');
    const counter = widget.querySelector('[data-like-count]');
    const unauthNotice = document.querySelector('[data-like-unauth]');
    const unauthClose = document.querySelector('[data-like-unauth-close]');

    const images = {
        like: widget.dataset.imgLike,
        liked: widget.dataset.imgLiked,
    };

    let liked = widget.dataset.liked === 'true';
    const authenticated = widget.dataset.authenticated === 'true';

    const render = () => {
        icon.src = liked ? images.liked : images.like;
        button.setAttribute('aria-pressed', liked ? 'true' : 'false');
    };

    // «пружинка» вместо растрового GIF: та же анимация, но векторная
    const animate = () => {
        icon.classList.remove('is-popping');
        void icon.offsetWidth; // перезапуск анимации
        icon.classList.add('is-popping');
        window.setTimeout(() => icon.classList.remove('is-popping'), 650);
    };

    render();

    button.addEventListener('click', async () => {
        if (!authenticated) {
            if (unauthNotice) {
                unauthNotice.hidden = false;
            }
            return;
        }

        button.disabled = true;
        try {
            const { ok, data } = await postJson(widget.dataset.url, {
                media_id: widget.dataset.mediaId,
            });

            if (!ok || !data.success) {
                console.error('like failed:', data.error);
                return;
            }

            liked = Boolean(data.liked);
            counter.textContent = data.likes_count;
            if (liked) {
                animate();
            } else {
                render();
            }
        } catch (error) {
            console.error('like request failed:', error);
        } finally {
            button.disabled = false;
        }
    });

    if (unauthClose && unauthNotice) {
        unauthClose.addEventListener('click', () => {
            unauthNotice.hidden = true;
        });
    }
}

initLikeWidget();
