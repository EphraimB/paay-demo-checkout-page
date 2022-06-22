var loginPopup = document.getElementById("loginPopup");
function highlightNavItem() {
    var links = document.getElementById("divWheel");
  
    for(var i = 0; i < links.children.length; i++) {
      if(links.children[i].children[0].pathname == window.location.pathname) {
        return i;
      }
    }

    return 0;
  }

var highlighttedNav = highlightNavItem();
var wheel = new wheelnav("divWheel", null, 300, 300);
wheel.slicePathFunction = slicePath().DonutSlice;
wheel.slicePathCustom = slicePath().DonutSliceCustomization();
wheel.maxPercent = 1.0;

wheel.slicePathCustom.minRadiusPercent = 0.3;
wheel.slicePathCustom.maxRadiusPercent = 0.6;
wheel.sliceSelectedPathCustom = wheel.slicePathCustom;
wheel.sliceInitPathCustom = wheel.slicePathCustom;

wheel.spreaderEnable = true;
wheel.spreaderInTitle = "imgsrc:/static/icons/login.svg"
wheel.spreaderOutTitle = "imgsrc:/static/icons/login.svg"
wheel.spreaderInPercent = 1.0;
wheel.spreaderOutPercent = 1.0;
wheel.spreaderRadius = wheel.wheelRadius * 0.25;
wheel.spreaderPathInAttr = { fill: '#FFF' };
wheel.spreaderPathOutAttr = { fill: '#FFF' }

wheel.createWheel();
wheel.navigateWheel(highlighttedNav);
wheel.setTooltips(["Home", "Cart"]);
wheel.sliceSelectedAttr = { stroke: '#111111', 'stroke-width': 4 };
wheel.refreshWheel()

var wheelspreader = document.getElementById("wheelnav-divWheel-spreader");
var wheelspreadertitle = document.getElementById("wheelnav-divWheel-spreadertitle");

wheelspreader.onmouseup = function() {
  if(loginPopup.className == "d-none") {
    showLoginPopup()
  } else {
    hidePopup()
  }
  openSpreader();
}
wheelspreadertitle.onmouseup = function() {
  if(loginPopup.className == "d-none") {
    showLoginPopup()
  } else {
    hidePopup()
  }
  openSpreader();
}

function showLoginPopup() {
  loginPopup.classList.remove("d-none");
  loginPopup.classList.add("d-flex", "position-absolute", "top-50", "start-50", "translate-middle", "card", "text-bg-light");
}

function hidePopup() {
  loginPopup.classList.remove("d-flex", "position-absolute", "top-50", "start-50", "translate-middle", "card", "text-bg-light");
  loginPopup.classList.add("d-none");
}

var openSpreader = function() {
  wheel.minPercent = wheel.maxPercent;
}