document.getElementById("cpf").addEventListener("input", function (e) {
    let cpf = e.target.value.replace(/\D/g, "");

    if (cpf.length > 3) {
        cpf = cpf.replace(/^(\d{3})/, "$1.");
    }
    if (cpf.length > 7) {
        cpf = cpf.replace(/^(\d{3})\.(\d{3})/, "$1.$2.");
    }
    if (cpf.length > 11) {
        cpf = cpf.replace(/^(\d{3})\.(\d{3})\.(\d{3})/, "$1.$2.$3-");
    }

    cpf = cpf.substring(0, 14);
    e.target.value = cpf;

    document.getElementById("cpf_sem_formatacao").value =
        e.target.value.replace(/\D/g, "");
});
