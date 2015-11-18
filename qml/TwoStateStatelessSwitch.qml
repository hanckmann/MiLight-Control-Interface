import QtQuick 2.0

Rectangle {
    id: statelessSwitch
    width: parent.width
    height: parent.height
    color: "transparent"

    property string name: "statelessSwitch"
    property string dragAreaColor: "yellow"
    property string dragAreaBorderColor: "blue"
    property string sliderColor: "red"
    property string sliderBorderColor: sliderColor

    objectName: name
    signal state1(string name)
    signal state2(string name)

    Rectangle {
        id: dragArea
        width: parent.width - (parent.border.width * 2)
        height: parent.height - (parent.border.width * 2)
        color: statelessSwitch.dragAreaColor

        border.width: 1
        border.color: statelessSwitch.dragAreaBorderColor
        radius: (parent.height - 10) / 2
        antialiasing : true

        MouseArea {
            id: mouseClickArea
            anchors.fill: parent

            onReleased: {
                if (mouse.y < height / 2) {
                    statelessSwitch.state1(statelessSwitch.name)
                }
                if (mouse.y > height / 2) {
                    statelessSwitch.state2(statelessSwitch.name)
                }
            }
        }

        Rectangle {
            property int btnWidth: parent.width - 2
            property int btnHeight: parent.height / 2
            property int centerY: (parent.height / 2) - (btnHeight / 2)
            property bool startAnime: false

            id: slider
            width: btnWidth
            height: btnHeight
            color: statelessSwitch.sliderColor

            anchors.horizontalCenter: parent.horizontalCenter

            y: centerY

            border.width: 1
            border.color: statelessSwitch.sliderBorderColor
            radius: btnWidth / 2

            Behavior on y {
                NumberAnimation {
                    duration: 500
                    easing.type: Easing.OutBounce
                }
            }

            Drag.active: mouseArea.drag.active

            MouseArea {
                id: mouseArea
                anchors.fill: parent

                drag.target: parent
                drag.axis: Drag.YAxis
                drag.minimumY: parent.x
                drag.maximumY: parent.height

                onReleased: {
                    if (slider.y < dragArea.height * .10) {
                        statelessSwitch.state1(statelessSwitch.name)
                    }
                    if (slider.y + parent.btnHeight > dragArea.height * .90) {
                        statelessSwitch.state2(statelessSwitch.name)
                    }
                    parent.y = slider.centerY
                }
            }
        }
    }
}