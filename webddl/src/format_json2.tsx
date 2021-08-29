import React, {Component} from 'react';
import JSONEditor from 'jsoneditor';
import isEqual from 'lodash/isEqual';
import cloneDeep from 'lodash/cloneDeep';
import 'jsoneditor/dist/jsoneditor.css';


interface IProps {
    schema?: {}
    json?: {}
    text: string
    mode?: string,
    indentation?: any,
    // onChangeText(text: string): any,
    // onModeChange(mode: string): any
}

interface IState {
}

class JsonEditor extends React.PureComponent<IProps, IState> {
    private readonly wrapper: React.RefObject<HTMLDivElement>;
    private jsonEditor: any;
    private schema: any;
    
    constructor(props: IProps) {
        super(props);
        this.wrapper = React.createRef();
    }


    componentDidMount () {
        // copy all properties into options for the editor
        // (except the properties for the JSONEditorReact component itself)
        let options = Object.assign({}, this.props);
        // delete options.json;
        // delete options.text;

        // @ts-ignore
        this.jsonEditor = new JSONEditor(this.wrapper.current, options);

        if ('json' in this.props) {
            this.jsonEditor.set(this.props.json);
        }
        if ('text' in this.props) {
            this.jsonEditor.setText(this.props.text);
        }

        this.schema = cloneDeep(this.props.schema);
        // this.schemaRefs = cloneDeep(this.props.schemaRefs);
    }

    // 更新
    componentDidUpdate() {
        if ('json' in this.props) {
            this.jsonEditor.update(this.props.json);
        }

        if ('text' in this.props) {
            this.jsonEditor.updateText(this.props.text);
        }

        if ('mode' in this.props) {
            this.jsonEditor.setMode(this.props.mode);
        }

        // store a clone of the schema to keep track on when it actually changes.
        // (When using a PureComponent all of this would be redundant)
        const schemaChanged = !isEqual(this.props.schema, this.schema);
        // const schemaRefsChanged = !isEqual(this.props.schemaRefs, this.schemaRefs);
        if (schemaChanged) {
            this.schema = cloneDeep(this.props.schema);
            // this.schemaRefs = cloneDeep(this.props.schemaRefs);
            this.jsonEditor.setSchema(this.props.schema);
        }
    }

    componentWillUnmount () {
        if (this.jsonEditor) {
            this.jsonEditor.destroy();
        }
    }

    render() {
        return (
            <div className="jsoneditor-react-container" ref={this.wrapper} />
        );
    }
}



export default JsonEditor