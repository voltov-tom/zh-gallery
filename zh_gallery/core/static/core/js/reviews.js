// Редактирование и удаление своих комментариев в личном кабинете.
// Разметку отзывов рендерит Django (никакого innerHTML с пользовательским
// текстом), JS только переключает режимы и отправляет запросы.

const csrfToken = () => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.content : '';
};

async function postJson(url, payload) {
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

function initReview(app, item) {
    const reviewId = item.dataset.reviewId;
    const text = item.querySelector('[data-review-text]');
    const form = item.querySelector('[data-review-edit]');
    const textarea = item.querySelector('[data-review-textarea]');
    const errorBox = item.querySelector('[data-review-error]');
    const editedBadge = item.querySelector('[data-review-edited]');

    if (!text || !form || !textarea) {
        return;
    }

    const openEdit = () => {
        textarea.value = text.textContent.trim();
        form.hidden = false;
        text.hidden = true;
        if (errorBox) {
            errorBox.hidden = true;
        }
    };

    const closeEdit = () => {
        form.hidden = true;
        text.hidden = false;
    };

    const showError = (message) => {
        if (errorBox) {
            errorBox.textContent = message;
            errorBox.hidden = false;
        }
    };

    item.addEventListener('click', async (event) => {
        const action = event.target.closest('[data-action]')?.dataset.action;
        if (!action) {
            return;
        }

        if (action === 'edit') {
            openEdit();
        } else if (action === 'cancel') {
            closeEdit();
        } else if (action === 'delete') {
            if (!window.confirm('Удалить комментарий?')) {
                return;
            }
            const { ok, data } = await postJson(app.dataset.deleteUrl, { review_id: reviewId });
            if (ok && data.success) {
                item.remove();
            } else {
                showError(data.error || 'не удалось удалить комментарий');
            }
        }
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const content = textarea.value.trim();
        if (!content) {
            showError('Комментарий не может быть пустым');
            return;
        }
        if (content === text.textContent.trim()) {
            closeEdit();
            return;
        }

        const { ok, data } = await postJson(app.dataset.editUrl, {
            review_id: reviewId,
            content,
        });

        if (ok && data.success) {
            text.textContent = data.content;
            if (editedBadge) {
                editedBadge.hidden = !data.edited;
            }
            closeEdit();
        } else {
            showError(data.error || 'не удалось сохранить комментарий');
        }
    });
}

function init() {
    const app = document.querySelector('[data-reviews-app]');
    if (!app) {
        return;
    }
    app.querySelectorAll('[data-review-item]').forEach((item) => initReview(app, item));
}

init();
