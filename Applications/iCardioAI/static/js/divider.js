var handler = document.querySelector('.handler');
var wrapper = handler.closest('body');
var boxA = wrapper.querySelector('.boxA');
var boxB = wrapper.querySelector('.boxB');
var initialBoxAWidth = boxA.offsetWidth;
var initialBoxBWidth = boxB.offsetWidth;
var isHandlerDragging = false;

document.addEventListener('mousedown', function(e) {
  // If mousedown event is fired from .handler, toggle flag to true
  if (e.target === handler) {
    isHandlerDragging = true;
  }
});

document.addEventListener('mousemove', function(e) {
  // Don't do anything if dragging flag is false
  if (!isHandlerDragging) {
    return false;
  }

  // Get offset
  var containerOffsetLeft = wrapper.offsetLeft;

  // Get x-coordinate of pointer relative to container
  var pointerRelativeXpos = e.clientX - containerOffsetLeft;
  
  // Arbitrary minimum width set on box A, otherwise its inner content will collapse to width of 0
  var boxAminWidth = 150;

  // Resize box A
  // * 8px is the left/right spacing between .handler and its inner pseudo-element
  // * Set flex-grow to 0 to prevent it from growing
  boxA.style.width = (Math.max(boxAminWidth, pointerRelativeXpos - 10)) + 'px';
  boxA.style.flexGrow = 0;
  boxB.style.width = initialBoxBWidth + (initialBoxAWidth -pointerRelativeXpos + 10) + 'px';
  handler.style.right = "calc(80% + " + (initialBoxAWidth -pointerRelativeXpos + 10) + "px)";
});

document.addEventListener('mouseup', function(e) {
  // Turn off dragging flag when user mouse is up
  isHandlerDragging = false;
});