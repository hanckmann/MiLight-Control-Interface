import QtQuick 2.2
import QtQuick.Window 2.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.1

ApplicationWindow {
    title: qsTr("Test Invoke")
    width: 500
    height: 500
    /*
    Row {
        spacing: 5

        Repeater {
            model: 4
            delegate: Rectangle {
                width: 40
                height: 120
                anchors.bottom: parent.bottom

                TwoStateStatelessSwitch {
                    name: 'group_' + (index + 1)
                    objectName: 'onoff'
                }
            }
        }
    }
    */

    Column {
        Row {
            Rectangle {
                width: 40
                height: 120
                anchors.bottom: parent.bottom

                TwoStateStatelessSwitch {
                    name: 'group_0'
                }
            }

            Rectangle {
                width: 40
                height: 120
                anchors.bottom: parent.bottom
            }

            Rectangle {
                width: 40
                height: 120
                anchors.bottom: parent.bottom

                TwoStateStatelessSwitch {
                    name: 'warmth'
                }
            }

            Rectangle {
                width: 40
                height: 120
                anchors.bottom: parent.bottom

                TwoStateStatelessSwitch {
                    name: 'brightness'
                }
            }
        }
        Row {
            Rectangle {
                width: 40
                height: 120
                anchors.bottom: parent.bottom

                TwoStateStatelessSwitch {
                    name: 'group_1'
                }
            }

            Rectangle {
                width: 40
                height: 120
                anchors.bottom: parent.bottom

                TwoStateStatelessSwitch {
                    name: 'group_2'
                }
            }
            Rectangle {
                width: 40
                height: 120
                anchors.bottom: parent.bottom

                TwoStateStatelessSwitch {
                    name: 'group_3'
                }
            }

            Rectangle {
                width: 40
                height: 120
                anchors.bottom: parent.bottom

                TwoStateStatelessSwitch {
                    name: 'group_4'
                }
            }
        }
    }
}