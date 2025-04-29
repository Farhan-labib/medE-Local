const Toast = {
    count: 0,

    init() {
        const toastNotification = document.createElement("div");
        toastNotification.className = "toast-notification";
        document.body.append(toastNotification);
    },

    show(message, type, seconds) {
        const toast = document.createElement("div");
        const check = document.createElement("ion-icon");
        const mssge = document.createElement("div");
        const cross = document.createElement("div");
        let hideTimeout = null;

        toast.className = `toast-content toast-${type}`;
        toast.id = ++this.count;

        check.name = "checkmark-outline";
        check.className = "check";

        mssge.textContent = message;
        mssge.className = "message";

        cross.innerHTML = `<ion-icon name="close-outline"></ion-icon>`;
        cross.className = "close";

        toast.append(check, mssge, cross);

        setTimeout(() => {
            document.querySelector(".toast-notification").append(toast);
        }, 5);

        setTimeout(() => {
            toast.classList.add("active");
        }, 10);

        cross.addEventListener("click", () => this.removeToast(document.getElementById(toast.id)));

        clearTimeout(hideTimeout);
        hideTimeout = setTimeout(() => {
            this.removeToast(document.getElementById(toast.id));
        }, seconds * 1000);
    },

    setRemainingTime() {
        // Function reserved for potential progress bar or countdown timer
    },

    removeToast(toast) {
        toast.classList.remove("active");
        toast.addEventListener("transitionend", () => {
            toast.remove();
        });
    },
};

Toast.init();

setTimeout(() => {
    document.querySelector(".addtocart").addEventListener("click", () => {
        Toast.show("Items added to cart!", "success", 2);
    });
}, 5);

document.querySelector(".addtolist2").addEventListener("click", () => {
    Toast.show("Items added to list!", "success", 2);
});
