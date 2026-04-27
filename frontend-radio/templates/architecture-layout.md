# Architecture Diagram Layout Template

Use this as the base JSON structure for every frontend architecture diagram.
Substitute the labeled placeholders with product-specific content.

## Canvas Overview

```
y=80   [SERVER BOX — full width, dark]
         ↓ arrow labeled with API protocol
y=280  [CONTROLLER BOX — full width, blue]
         ↙ arrow (reads/writes)    ↘ arrow (dispatches)
y=500  [CLIENT STORE — left, orange]   [VIEW CONTAINER — right, green]
                                        [Sub-view 1]
                                        [Sub-view 2]
                                        [Sub-view 3]
```

## Base JSON Template

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [

    // ─── SERVER ───────────────────────────────────────────────────────────
    {
      "type": "rectangle", "id": "server",
      "x": 200, "y": 80, "width": 900, "height": 100,
      "strokeColor": "#212529", "backgroundColor": "#343a40",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1001,
      "groupIds": [], "frameId": null, "roundness": {"type": 3},
      "boundElements": [{"id": "t_server", "type": "text"}],
      "updated": 1, "link": null, "locked": false,
      "version": 1, "versionNonce": 1001, "isDeleted": false
    },
    {
      "type": "text", "id": "t_server",
      "x": 200, "y": 80, "width": 900, "height": 100,
      "containerId": "server",
      "text": "SERVER\n(GET /api/<resource> · POST /api/<resource>)",
      "fontFamily": 5, "fontSize": 18,
      "textAlign": "center", "verticalAlign": "middle",
      "strokeColor": "#f8f9fa", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1002,
      "groupIds": [], "frameId": null, "roundness": null,
      "boundElements": null, "updated": 1, "link": null, "locked": false,
      "lineHeight": 1.25, "baseline": 22,
      "version": 1, "versionNonce": 1002, "isDeleted": false
    },

    // ─── SERVER → CONTROLLER ARROW ───────────────────────────────────────
    {
      "type": "arrow", "id": "arr_s_c",
      "x": 650, "y": 180, "width": 0, "height": 100,
      "points": [[0, 0], [0, 100]],
      "strokeColor": "#1971c2", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1003,
      "groupIds": [], "frameId": null, "roundness": {"type": 2},
      "boundElements": [{"id": "t_arr_s_c", "type": "text"}],
      "startBinding": null, "endBinding": null,
      "startArrowhead": "arrow", "endArrowhead": "arrow",
      "lastCommittedPoint": null,
      "updated": 1, "link": null, "locked": false,
      "version": 1, "versionNonce": 1003, "isDeleted": false
    },
    {
      "type": "text", "id": "t_arr_s_c",
      "x": 660, "y": 220, "width": 120, "height": 20,
      "containerId": "arr_s_c",
      "text": "HTTP / WebSocket",
      "fontFamily": 5, "fontSize": 12,
      "textAlign": "center", "verticalAlign": "middle",
      "strokeColor": "#1971c2", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1004,
      "groupIds": [], "frameId": null, "roundness": null,
      "boundElements": null, "updated": 1, "link": null, "locked": false,
      "lineHeight": 1.25, "baseline": 15,
      "version": 1, "versionNonce": 1004, "isDeleted": false
    },

    // ─── CONTROLLER ──────────────────────────────────────────────────────
    {
      "type": "rectangle", "id": "controller",
      "x": 200, "y": 280, "width": 900, "height": 100,
      "strokeColor": "#1971c2", "backgroundColor": "#a5d8ff",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1005,
      "groupIds": [], "frameId": null, "roundness": {"type": 3},
      "boundElements": [{"id": "t_ctrl", "type": "text"}],
      "updated": 1, "link": null, "locked": false,
      "version": 1, "versionNonce": 1005, "isDeleted": false
    },
    {
      "type": "text", "id": "t_ctrl",
      "x": 200, "y": 280, "width": 900, "height": 100,
      "containerId": "controller",
      "text": "CONTROLLER\n(handles user events · calls server APIs · updates store · transforms data for view)",
      "fontFamily": 5, "fontSize": 15,
      "textAlign": "center", "verticalAlign": "middle",
      "strokeColor": "#1864ab", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1006,
      "groupIds": [], "frameId": null, "roundness": null,
      "boundElements": null, "updated": 1, "link": null, "locked": false,
      "lineHeight": 1.25, "baseline": 19,
      "version": 1, "versionNonce": 1006, "isDeleted": false
    },

    // ─── CONTROLLER → STORE ARROW ────────────────────────────────────────
    {
      "type": "arrow", "id": "arr_c_store",
      "x": 380, "y": 380, "width": 0, "height": 120,
      "points": [[0, 0], [0, 120]],
      "strokeColor": "#e67700", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 1.5, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1007,
      "groupIds": [], "frameId": null, "roundness": {"type": 2},
      "startBinding": null, "endBinding": null,
      "startArrowhead": null, "endArrowhead": "arrow",
      "lastCommittedPoint": null, "boundElements": null,
      "updated": 1, "link": null, "locked": false,
      "version": 1, "versionNonce": 1007, "isDeleted": false
    },

    // ─── CONTROLLER → VIEW ARROW ─────────────────────────────────────────
    {
      "type": "arrow", "id": "arr_c_view",
      "x": 900, "y": 380, "width": 0, "height": 120,
      "points": [[0, 0], [0, 120]],
      "strokeColor": "#2b8a3e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 1.5, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1008,
      "groupIds": [], "frameId": null, "roundness": {"type": 2},
      "startBinding": null, "endBinding": null,
      "startArrowhead": null, "endArrowhead": "arrow",
      "lastCommittedPoint": null, "boundElements": null,
      "updated": 1, "link": null, "locked": false,
      "version": 1, "versionNonce": 1008, "isDeleted": false
    },

    // ─── CLIENT STORE ─────────────────────────────────────────────────────
    {
      "type": "rectangle", "id": "store",
      "x": 200, "y": 500, "width": 320, "height": 280,
      "strokeColor": "#e67700", "backgroundColor": "#ffd8a8",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1009,
      "groupIds": [], "frameId": null, "roundness": {"type": 3},
      "boundElements": [{"id": "t_store", "type": "text"}],
      "updated": 1, "link": null, "locked": false,
      "version": 1, "versionNonce": 1009, "isDeleted": false
    },
    {
      "type": "text", "id": "t_store",
      "x": 200, "y": 500, "width": 320, "height": 280,
      "containerId": "store",
      "text": "CLIENT STORE\n\n<entity_1>[]\n<entity_2>[]\n<user>: User\npagination: Cursor",
      "fontFamily": 5, "fontSize": 14,
      "textAlign": "center", "verticalAlign": "middle",
      "strokeColor": "#7c4a03", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1010,
      "groupIds": [], "frameId": null, "roundness": null,
      "boundElements": null, "updated": 1, "link": null, "locked": false,
      "lineHeight": 1.25, "baseline": 17,
      "version": 1, "versionNonce": 1010, "isDeleted": false
    },

    // ─── VIEW CONTAINER ───────────────────────────────────────────────────
    {
      "type": "rectangle", "id": "view",
      "x": 580, "y": 500, "width": 520, "height": 360,
      "strokeColor": "#2b8a3e", "backgroundColor": "#d3f9d8",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1011,
      "groupIds": [], "frameId": null, "roundness": {"type": 3},
      "boundElements": [{"id": "t_view", "type": "text"}],
      "updated": 1, "link": null, "locked": false,
      "version": 1, "versionNonce": 1011, "isDeleted": false
    },
    {
      "type": "text", "id": "t_view",
      "x": 580, "y": 500, "width": 520, "height": 30,
      "containerId": "view",
      "text": "VIEW",
      "fontFamily": 5, "fontSize": 16,
      "textAlign": "center", "verticalAlign": "top",
      "strokeColor": "#1a5c2b", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1012,
      "groupIds": [], "frameId": null, "roundness": null,
      "boundElements": null, "updated": 1, "link": null, "locked": false,
      "lineHeight": 1.25, "baseline": 20,
      "version": 1, "versionNonce": 1012, "isDeleted": false
    },

    // ─── VIEW SUB-COMPONENTS (add one per component) ──────────────────────
    // Sub-component 1
    {
      "type": "rectangle", "id": "sub1",
      "x": 610, "y": 560, "width": 220, "height": 55,
      "strokeColor": "#40c057", "backgroundColor": "#ebfbee",
      "fillStyle": "solid", "strokeWidth": 1.5, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1013,
      "groupIds": [], "frameId": null, "roundness": {"type": 3},
      "boundElements": [{"id": "t_sub1", "type": "text"}],
      "updated": 1, "link": null, "locked": false,
      "version": 1, "versionNonce": 1013, "isDeleted": false
    },
    {
      "type": "text", "id": "t_sub1",
      "x": 610, "y": 560, "width": 220, "height": 55,
      "containerId": "sub1", "text": "<SubComponent1>",
      "fontFamily": 5, "fontSize": 13,
      "textAlign": "center", "verticalAlign": "middle",
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1014,
      "groupIds": [], "frameId": null, "roundness": null,
      "boundElements": null, "updated": 1, "link": null, "locked": false,
      "lineHeight": 1.25, "baseline": 16,
      "version": 1, "versionNonce": 1014, "isDeleted": false
    },

    // Sub-component 2
    {
      "type": "rectangle", "id": "sub2",
      "x": 610, "y": 640, "width": 220, "height": 55,
      "strokeColor": "#40c057", "backgroundColor": "#ebfbee",
      "fillStyle": "solid", "strokeWidth": 1.5, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1015,
      "groupIds": [], "frameId": null, "roundness": {"type": 3},
      "boundElements": [{"id": "t_sub2", "type": "text"}],
      "updated": 1, "link": null, "locked": false,
      "version": 1, "versionNonce": 1015, "isDeleted": false
    },
    {
      "type": "text", "id": "t_sub2",
      "x": 610, "y": 640, "width": 220, "height": 55,
      "containerId": "sub2", "text": "<SubComponent2>",
      "fontFamily": 5, "fontSize": 13,
      "textAlign": "center", "verticalAlign": "middle",
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1016,
      "groupIds": [], "frameId": null, "roundness": null,
      "boundElements": null, "updated": 1, "link": null, "locked": false,
      "lineHeight": 1.25, "baseline": 16,
      "version": 1, "versionNonce": 1016, "isDeleted": false
    },

    // Sub-component 3
    {
      "type": "rectangle", "id": "sub3",
      "x": 610, "y": 720, "width": 220, "height": 55,
      "strokeColor": "#40c057", "backgroundColor": "#ebfbee",
      "fillStyle": "solid", "strokeWidth": 1.5, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1017,
      "groupIds": [], "frameId": null, "roundness": {"type": 3},
      "boundElements": [{"id": "t_sub3", "type": "text"}],
      "updated": 1, "link": null, "locked": false,
      "version": 1, "versionNonce": 1017, "isDeleted": false
    },
    {
      "type": "text", "id": "t_sub3",
      "x": 610, "y": 720, "width": 220, "height": 55,
      "containerId": "sub3", "text": "<SubComponent3>",
      "fontFamily": 5, "fontSize": 13,
      "textAlign": "center", "verticalAlign": "middle",
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "angle": 0, "seed": 1018,
      "groupIds": [], "frameId": null, "roundness": null,
      "boundElements": null, "updated": 1, "link": null, "locked": false,
      "lineHeight": 1.25, "baseline": 16,
      "version": 1, "versionNonce": 1018, "isDeleted": false
    }
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

## Customization Notes

- **Add more sub-components**: Clone sub1/sub2/sub3 blocks, increment IDs and y coordinates by 80px each
- **Add a Router**: Add a box between Controller and View, labeled "Router", `backgroundColor: "#f3d9fa"`, `strokeColor: "#9c36b5"`
- **WebSocket**: Change the Server→Controller arrow label to "WebSocket" and make it `strokeStyle: "dashed"`
- **Multiple stores**: Add sibling boxes next to the Client Store, same color scheme
- **Event bus / PubSub**: Add a central hub box if the design has many-to-many component communication
