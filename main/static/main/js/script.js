document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".allPaths").forEach(e => {
        e.addEventListener("mouseover", function () {
            console.log(`Hovered over: ${e.id}`); // Debugging Log

            // Highlight country
            e.style.fill = "pink";

            // Show tooltip with country name
            const nameTag = document.getElementById("name");
            const namep = document.getElementById("namep");

            if (nameTag && namep) {
                nameTag.style.opacity = 1;
                namep.innerText = e.id;
            }
        });

        e.addEventListener("mouseleave", function () {
            console.log(`Mouse left: ${e.id}`); // Debugging Log

            // Revert country color
            e.style.fill = "#ececec";

            // Hide tooltip
            document.getElementById("name").style.opacity = 0;
        });

        e.addEventListener("click", function () {
            alert(`Clicked on: ${e.id}`); // Replace with your function
        });
    });

    // Track mouse movement to update tooltip position
    window.addEventListener("mousemove", function (j) {
        let x = j.clientX;
        let y = j.clientY;
        const nameTag = document.getElementById('name');

        if (nameTag) {
            nameTag.style.top = (y - 60) + 'px';
            nameTag.style.left = (x + 10) + 'px';
        }
    });
});
