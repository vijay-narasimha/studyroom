const listContainer = document.querySelector("[data-listContainer]");
const lists = document.querySelector(".lists");
const listForm = document.querySelector(".list-form");
const listBtn = document.querySelector(".list-btn");
const listInput = document.querySelector(".list-input");
const deleteList = document.querySelector(".clearlist");
const taskContainer = document.querySelector(".task-container-1");
const taskTitle = document.querySelector(".task-title");
const taskLists = document.querySelector(".task-list");
const taskForm = document.querySelector(".task-form");
const taskInput = document.querySelector(".task-input");
const taskBtn = document.querySelector(".task-btn");
const clearalltasks = document.querySelector(".clearalltasks");

let todos = JSON.parse(localStorage.getItem("todo-list")) || [];
let selectedId = JSON.parse(localStorage.getItem("selected-list"));
listForm.addEventListener("submit", (e) => {
	e.preventDefault();
	listBtn.click();
});
taskForm.addEventListener("submit", (e) => {
	e.preventDefault();
	taskBtn.click();
});
listBtn.addEventListener("click", (e) => {
	e.preventDefault();
	if (listInput.value == null || listInput.value === "") return;

	const newList = {
		id: Date.now().toString(),
		name: listInput.value,
		tasks: [],
	};
	listInput.value = "";

	todos.push(newList);

	saveandrender();
});
taskBtn.addEventListener("click", (e) => {
	e.preventDefault();
	if (taskInput.value == null || taskInput.value === "") return;
	const newTask = {
		id: Date.now().toString(),
		name: taskInput.value,
		complete: false,
	};
	taskInput.value = "";
	const selectedList = todos.find((list) => list.id === selectedId);
	selectedList.tasks.push(newTask);
	saveandrender();
});
taskLists.addEventListener("click", (e) => {
	if (e.target.tagName.toLowerCase() === "input") {
		const selectedList = todos.find((list) => list.id === selectedId);
		const selectedTask = selectedList.tasks.find(
			(task) => task.id === e.target.id,
		);
		selectedTask.complete = e.target.checked;
		
		save();
	}
});
function saveandrender() {
	save();
	render();
}
function save() {
	localStorage.setItem("todo-list", JSON.stringify(todos));
	localStorage.setItem("selected-list", JSON.stringify(selectedId));
}
function render() {
	clearelement(lists);
	let li = "";

	if (!todos) return;
	todos.forEach((todo) => {
		li += `<li data-id=${todo.id} class=${
			todo.id === selectedId ? "active" : ""
		}>${todo.name}</li>`;
	});
	lists.innerHTML = li;

	const selectedList = todos.find((list) => list.id === selectedId);
	if (!selectedId) {
		taskContainer.style.display = "none";
	} else {
		taskContainer.style.display = "";
		taskTitle.innerText = selectedList.name;
		clearelement(taskLists);
		let div = "";
		selectedList.tasks.forEach((task) => {
			div += `<div class="task">
<input type="checkbox" id=${task.id} ${task.complete?'checked':" "} />
<label for=${task.id}>
    <span class="custom-checkbox"></span>
    <p >${task.name}</p>
</label>
</div>`;
		});
		taskLists.innerHTML = div;
	}
}
function clearelement(element) {
	while (element.firstChild) {
		element.removeChild(element.firstChild);
	}
}
render();
lists.addEventListener("click", (e) => {
	if (e.target.tagName.toLowerCase() === "li") {
		selectedId = e.target.dataset.id;

		saveandrender();
	}
});
deleteList.addEventListener("click", () => {
	todos = todos.filter((list) => list.id !== selectedId);
	selectedId = null;
	saveandrender();
});
clearalltasks.addEventListener("click", (e) => {
	const selectedList = todos.find((list) => list.id === selectedId);
	selectedList.tasks = selectedList.tasks.filter((task) => !task.complete);
	saveandrender();
});
