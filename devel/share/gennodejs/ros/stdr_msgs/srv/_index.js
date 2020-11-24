
"use strict";

let LoadExternalMap = require('./LoadExternalMap.js')
let AddSoundSource = require('./AddSoundSource.js')
let AddCO2Source = require('./AddCO2Source.js')
let DeleteCO2Source = require('./DeleteCO2Source.js')
let RegisterGui = require('./RegisterGui.js')
let DeleteThermalSource = require('./DeleteThermalSource.js')
let DeleteRfidTag = require('./DeleteRfidTag.js')
let LoadMap = require('./LoadMap.js')
let AddRfidTag = require('./AddRfidTag.js')
let AddThermalSource = require('./AddThermalSource.js')
let MoveRobot = require('./MoveRobot.js')
let DeleteSoundSource = require('./DeleteSoundSource.js')

module.exports = {
  LoadExternalMap: LoadExternalMap,
  AddSoundSource: AddSoundSource,
  AddCO2Source: AddCO2Source,
  DeleteCO2Source: DeleteCO2Source,
  RegisterGui: RegisterGui,
  DeleteThermalSource: DeleteThermalSource,
  DeleteRfidTag: DeleteRfidTag,
  LoadMap: LoadMap,
  AddRfidTag: AddRfidTag,
  AddThermalSource: AddThermalSource,
  MoveRobot: MoveRobot,
  DeleteSoundSource: DeleteSoundSource,
};
