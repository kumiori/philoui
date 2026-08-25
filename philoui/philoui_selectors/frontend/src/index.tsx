import React from "react"
import ReactDOM from "react-dom"
import QualitativeSelector from "./QualitativeSelector"
import QualitativeParametricSelector from "./ParametricQualitativeSelector"
import Dichotomy from "./Dichotomy"
import { ComponentProps, withStreamlitConnection } from "streamlit-component-lib";

const QualiQuantiComponent = (props: ComponentProps) => {
  //get data
  const component = props.args['component']
  // Return the requested selector while keeping one Streamlit connection.
  switch (component) {
    case 'dichotomy':
      return <Dichotomy {...props} />;
    case 'qualitative':
      return <QualitativeSelector {...props} />;
      case 'parametric':
      return <QualitativeParametricSelector {...props} />;
    default:
      return <p>Unknown selector type.</p>
  }
};

const StreamlitQualiQuantiComponent = withStreamlitConnection(QualiQuantiComponent)

ReactDOM.render(
  <StreamlitQualiQuantiComponent />,
  document.getElementById("root")
)
