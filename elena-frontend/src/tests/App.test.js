import React from "react";
import { render } from "@testing-library/react";
import { App } from "../App";

describe("App Component", function () {
    it("Should display the component and the overlay", function () {
        global.URL.createObjectURL = jest.fn();
        let app = render(<App />);
        expect(app.getByText("Minimize Elevation"))
    });
});