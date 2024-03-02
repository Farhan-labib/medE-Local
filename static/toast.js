const Toast = {
    count: 0,
    init() {
        let toastNotification = document.createElement("div");
        toastNotification.className = "toast-notification";
        document.body.append(toastNotification);
    },

    show(message, type, seconds) {
        // console.log(localStorage.getItem('cart'));
        let toast = document.createElement("div");
        let check = document.createElement("ion-icon");
        let mssge = document.createElement("div");
        let cross = document.createElement("div");
        let hideTimeout = null;

        toast.className = "toast-content";
        mssge.textContent = message;
        mssge.className = "message";
        check.name = "checkmark-outline";
        check.className = "check";
        cross.innerHTML = `<ion-icon name="close-outline"></ion-icon>`;
        cross.className = "close";
        toast.id = ++this.count;

        this.setRemainingTime(toast, seconds);

        toast.classList = (`toast-content toast-${type}`);


        toast.append(check, mssge);
        toast.appendChild(cross);

        setTimeout(() => {
            document.querySelector(".toast-notification").append(toast);
        }, 5);
        setTimeout(() => {
            toast.classList.add("active");
        }, 10);
        // toast.textContent = message;
        // toast.textContent.className = "message";

        // console.log(deleteId);

        cross.addEventListener("click", () => this.removeToast(document.getElementById(toast.id)));

        clearTimeout(hideTimeout);

        hideTimeout = setTimeout(() => {
            this.removeToast(document.getElementById(toast.id));
        }, seconds * 1000);
    },

    setRemainingTime() {
    },

    removeToast(deleteId) {
        deleteId.classList.remove("active");
        deleteId.addEventListener("transitionend", () => {
            deleteId.remove();
        });
    },

};

// document.querySelector(".addtolist").addEventListener("click", () =>{
//     count++;
//     console.log(count);
//     toastContainer.append(`
//     <div class="toast-content">
//     <ion-icon class="check" name="checkmark-outline"></ion-icon>

//     <div class="message">
//     <span class="text text-1">Items added to list!</span>
//     </div>
//     </div>
//     <ion-icon class="close" name="close-outline"></ion-icon>
//     <div class="progress"></div>
//     `)
//     document.querySelector(".toast-notification").classList.add("active");
//     document.querySelector(".progress").classList.add("active");
//     // document.querySelector(".toast-notification").style.display = "block";
//     setTimeout(() =>{
//         document.querySelector(".toast-notification").classList.remove("active");
//     }, 5000);
// });

// document.querySelector(".close").addEventListener("click", () =>{
//     document.querySelector(".toast-notification").classList.remove("active");
// });

Toast.init();
setTimeout(() => {

    document.querySelector(".addtocart").addEventListener("click", () => {
        // document.querySelector(".toast-notification").classList.add("active");
        Toast.show("Items added to cart!", "success", 2);
    });
}, 5);
document.querySelector(".addtolist2").addEventListener("click", () => {
    // document.querySelector(".toast-notification").classList.add("active");
    Toast.show("Items added to list!", "success", 2);
});