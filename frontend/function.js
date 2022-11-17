function enableEditMode() {
    richTextField.document.designMode = "on";
  }
  function Edit(command) {
    richTextField.document.execCommand(command, false, null);
  }
  function execVal(command, value) {
    richTextField.document.execCommand(command, false, value);
  }