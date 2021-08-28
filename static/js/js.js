$(".main-alert-asd-2d2-wdq-")
  .fadeTo(2000, 500)
  .slideUp(500, function () {
    $(".main-alert-asd-2d2-wdq-").slideUp(500);
  });
var viewDataModal = document.getElementById("viewDataModal");
viewDataModal.addEventListener("show.bs.modal", function (event) {
  // Button that triggered the modal
  var button = event.relatedTarget;
  // Extract info from data-bs-* attributes
  var dataID = button.getAttribute("data-bs-dataID");
  fetch(`/get/${dataID}`, {
    method: "GET",
  })
    .then((resp) => resp.json())
    .then((fetched_data) => {
      viewDataModal.querySelector(".modal-title").textContent =
        fetched_data[0]["dataName"]; // this is for the modal title
      viewDataModal.querySelector("#modL0NamedISp").value =
        fetched_data[0]["dataName"]; // this is for the modal input dataName
      viewDataModal.querySelector("#disp-list").textContent =
        fetched_data[0]["list"]; // this is for the list data in the modal
      viewDataModal.querySelector("#update-si0Data-btn").value =
        fetched_data[0]["dataID"]; // this is to provide the update button with the dataId in order if the user wanted to update
    });
});
function unChngs() {
  document.getElementById("update-btn").disabled = false;
}
function paschng() {
  document.getElementById("updatePass-btn").disabled = false;
}
