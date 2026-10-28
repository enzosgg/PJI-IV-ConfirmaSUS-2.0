document.querySelectorAll("tbody tr").forEach((row) => {
    row.addEventListener("click", () => {
        const consulta_disponivel_id = row.getAttribute(
            "consulta-disponivel-id"
        );
        const consulta_id = document.getElementById("consulta-id").value;

        Swal.fire({
            title: "Confirmar reagendamento",
            text: "Deseja realmente reagendar esta consulta?",
            icon: "question",
            showCancelButton: true,
            confirmButtonColor: "#1abd14",
            cancelButtonColor: "#B60000",
            confirmButtonText: "Sim, reagendar!",
            cancelButtonText: "Não",
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = `/confirmar-reagendamento/${consulta_id}/${consulta_disponivel_id}/`;
            }
        });
    });
});
