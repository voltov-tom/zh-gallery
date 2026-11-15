// Подтверждение удаления адреса почты.
// Раньше это был инлайновый <script> в блоке extra_body, которого в base.html
// нет — то есть подтверждение вообще не срабатывало и адрес удалялся сразу.

const form = document.querySelector('.email_list[data-confirm]');
if (form) {
    const message = form.dataset.confirm;

    form.addEventListener('submit', (event) => {
        const action = event.submitter?.name;
        if (action !== 'action_remove') {
            return;
        }
        if (!window.confirm(message)) {
            event.preventDefault();
        }
    });
}
