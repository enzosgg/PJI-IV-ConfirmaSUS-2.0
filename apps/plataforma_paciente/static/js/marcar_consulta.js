document.querySelectorAll("tbody tr[consulta-disponivel-id]").forEach((row) => {
    row.addEventListener("click", () => {
        const consulta_disponivel_id = row.getAttribute(
            "consulta-disponivel-id"
        );

        Swal.fire({
            title: "Confirmar marcação",
            text: "Deseja realmente marcar esta consulta?",
            icon: "question",
            showCancelButton: true,
            confirmButtonColor: "#1abd14",
            cancelButtonColor: "#B60000",
            confirmButtonText: "Sim, marcar!",
            cancelButtonText: "Não",
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = `/confirmar_marcacao/${consulta_disponivel_id}/`;
            }
        });
    });
});
