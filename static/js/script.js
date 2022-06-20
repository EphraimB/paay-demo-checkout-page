function highlightNavItem() {
    var links = document.getElementById("divWheel");
  
    for(var i = 0; i < links.length; i++) {
      if(window.location.pathname == "/") {
        return 0;
      } else if(window.location.pathname == "/everydayLife/" || window.location.pathname == "/college/") {
        return 2;
      } else if(links.children[i].pathname == window.location.pathname.match(new RegExp("^" + links.children[i].pathname,"g"))) {
        return i;
      }
    }

    return 0;
  }

// var highlighttedNav = highlightNavItem();
var wheel = new wheelnav("divWheel", null, 300, 300);
wheel.slicePathFunction = slicePath().DonutSlice;
wheel.slicePathCustom = slicePath().DonutSliceCustomization();
wheel.maxPercent = 1.0;

wheel.slicePathCustom.minRadiusPercent = 0.3;
wheel.slicePathCustom.maxRadiusPercent = 0.6;
wheel.sliceSelectedPathCustom = wheel.slicePathCustom;
wheel.sliceInitPathCustom = wheel.slicePathCustom;
wheel.createWheel();
// wheel.navigateWheel(highlighttedNav);
wheel.setTooltips(["Home", "Cart", "Login"]);
wheel.sliceSelectedAttr = { stroke: '#111111', 'stroke-width': 4 };
wheel.refreshWheel()