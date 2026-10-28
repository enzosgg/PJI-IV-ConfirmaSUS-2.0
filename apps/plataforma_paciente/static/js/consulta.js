document.addEventListener("DOMContentLoaded", function () {
    const btncancelar = document.getElementById("btncancelar");
    const btnconfirmar = document.getElementById("btnconfirmar");

    if (btncancelar) {
        btncancelar.addEventListener("click", function () {
            const consulta_id = this.getAttribute("consulta-id");

            Swal.fire({
                title: "Confirmar cancelamento",
                text: "Deseja realmente cancelar esta consulta?",
                icon: "question",
                showCancelButton: true,
                confirmButtonColor: "#1abd14",
                cancelButtonColor: "#d33",
                confirmButtonText: "Sim, cancelar!",
                cancelButtonText: "Não",
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = `/cancelar_consulta/${consulta_id}/`;
                }
            });
        });
    }

    if (btnconfirmar) {
        btnconfirmar.addEventListener("click", function () {
            const consulta_id = this.getAttribute("consulta-id");

            Swal.fire({
                title: "Confirmar presença na unidade",
                text: "Deseja realmente confirmar presença no hospital?",
                icon: "question",
                showCancelButton: true,
                confirmButtonColor: "#1abd14",
                cancelButtonColor: "#B60000",
                confirmButtonText: "Sim, estou aqui!",
                cancelButtonText: "Não",
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = `/confirmar_presenca/${consulta_id}/`;
                }
            });
        });
    }
});
