function habilitarEdicao(campoId) {
    const campo = document.getElementById(campoId);
    campo.removeAttribute('readonly');
    campo.focus();
}

function habilitarEdicaoSenha(campoId) {
    const campo = document.getElementById(campoId);
    campo.removeAttribute('readonly');
    campo.removeAttribute('value');
    campo.focus();
}