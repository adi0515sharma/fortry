/* ---------------------------------- NAVBAR  START -----------------------------------------------------*/
const notificationList = () => {
    var x = document.getElementsByClassName("notification-list")[0].style.display;
    if(x=="block")
      document.getElementsByClassName("notification-list")[0].style.display = "none";
    else  
      document.getElementsByClassName("notification-list")[0].style.display = "block";
  }
  
  
  /* ---------------------------------- NAVBAR END -----------------------------------------------------*/
  
  /* ---------------------------------- SIDEBAR  LIST-----------------------------------------------------*/
  const showEventList = () => {
    document.getElementsByClassName("event-list")[0].style.display = "block";
  }
  
  const hideEventList = () => {
    document.getElementsByClassName("event-list")[0].style.display = "none";
  }
  
  
  const showContactList = () => {
    document.getElementsByClassName("contact-list")[0].style.display = "block";
  }
  
  const hideContactList = () => {
    document.getElementsByClassName("contact-list")[0].style.display = "none";
  }
  
  const showReportList = () => {
    document.getElementsByClassName("report-list")[0].style.display = "block";
  }
  
  const hideReportList = () => {
    document.getElementsByClassName("report-list")[0].style.display = "none";
  }
  