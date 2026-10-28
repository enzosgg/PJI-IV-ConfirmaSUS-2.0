document.addEventListener("DOMContentLoaded", function () {
    const btncompareceu = document.getElementById("btncompareceu");
    const btnfaltou = document.getElementById("btnfaltou");

    if (btncompareceu) {
        btncompareceu.addEventListener("click", function () {
            Swal.fire({
                title: "Confirmar comparecimento",
                text: "Deseja realmente confirmar que o paciente compareceu?",
                icon: "question",
                showCancelButton: true,
                confirmButtonColor: "#1abd14",
                cancelButtonColor: "#B60000",
                confirmButtonText: "Sim, o paciente compareceu!",
                cancelButtonText: "Não",
            }).then((result) => {
                if (result.isConfirmed) {
                    const consulta_id = this.getAttribute("consulta-id");
                    window.location.href = `/paciente_compareceu/${consulta_id}/`;
                }
            });
        });
    }

    if (btnfaltou) {
        btnfaltou.addEventListener("click", function () {
            Swal.fire({
                title: "Paciente não compareceu",
                text: "Deseja realmente confirmar que o paciente não compareceu?",
                icon: "question",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: "Sim, o paciente não compareceu!",
                cancelButtonText: "Não",
            }).then((result) => {
                if (result.isConfirmed) {
                    const consulta_id = this.getAttribute("consulta-id");
                    window.location.href = `/paciente_faltou/${consulta_id}/`;
                }
            });
        });
    }
});
