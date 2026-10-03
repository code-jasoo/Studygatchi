import "./App.css";

export default function EditModal({ item, close }) {

  const saveTask = async () => {
    // TODO: Implement task saving here
    console.log("Save task.");
  }


  return (
    <div>
      <h3>Edit Task</h3>
      { item }
      <br/>
      <form className="editmodal-form">
        <div className="editmodal-field">
          <label>Name: </label>
          <input type="text" defaultValue={"Name"} />
        </div>
        <div className="editmodal-field">
          <label>Description: </label>
          <input type="text" defaultValue={"Description"} />
        </div>
        <div className="editmodal-field">
          <label>Category: </label>
          <input type="text" defaultValue={"Category"} />
        </div>
        <div className="editmodal-field">
          <label>Due Date: </label>
          <input type="date" defaultValue={"0000-00-00"}/>
        </div>
        <div className="editmodal-field">
          <label>Reward: </label>
          <input type="number" defaultValue={0} />
        </div>
      </form>
      <button onClick={() => saveTask()}>Save</button>
      <button onClick={() => close()}>Close</button>
    </div>
  )
}
