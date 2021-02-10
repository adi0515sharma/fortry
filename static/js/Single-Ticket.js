DecoupledEditor
    .create(document.querySelector('#editor-single-ticket'))
    .then(editor => {
        const toolbarContainer = document.querySelector('#toolbar-container-single-ticket');

        toolbarContainer.appendChild(editor.ui.view.toolbar.element);
    })
    .catch(error => {
        console.error(error);
    });