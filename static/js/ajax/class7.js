function buildTable(class_name, period) {
    // let table = document.getElementById("myTbody");
	let table = document.querySelector("#myTable tbody");
	// let thead = document.getElementById("myTHead");
	let thead = document.querySelector("#myTable thead");
	let modalCon = document.getElementById("modal-con");
	let url = "/api/classroom/";
	url += class_name + "/" + period;
	fetch(url)
		.then((res) => res.json())
		.then((data) => {
            let list = data["student_list"];
            let timetable = data["timetable"];
            let all_status = data["all_status"];
			thead.innerHTML += `
			<th>ID</th>
			<th>Name</th>
			<th>Status</th>
			<th>Modify</th>
			`
			list.forEach(val => {
                let item = `
                <tr>
				  	<td>${val.studentID}</td>
				  	<td>${val.name}</td>
				  	<td>
						<div class="status-box">
							<h3 style="color: ${val.status_color};">&#9679;</h3>
							<p>${val.status}</p>
						</div>
					</td>
				  	<td>
          				<button
          				type="button"
          				class="btn btn-primary edit-btn"
          				data-bs-toggle="modal"
          				data-bs-target="#id${val.studentID}"
						>
          				Edit
						</button>
          			</td>
        		</tr>
                `;      

                let form = `
                    <div class="modal fade" id="id${val.studentID}" tabindex="-1" aria-labelledby="ModalLabel" aria-hidden="true">
						<div class="modal-dialog">
							<div class="modal-content">
								<div class="modal-header">
								    <h5 class="modal-title" id="ModalLabel">
								    	Edit Status of ${val.name}
								    </h5>
								    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
								</div>
								<form method="post" action="/class/change-status/">
									<div class="modal-body d-flex flex-column">
										<div class="mb-3 row">
											<label for="ID" class="col-sm-2 col-form-label">ID</label>
											<div class="col-sm-10">
												<input
													type="text"
													readonly
													class="form-control-plaintext"
													id="ID"
													name="ID"
													value="${val.studentID}"
												/>
											</div>
										</div>
									
										<div class="mb-3 row">
											<label for="subjectChange" class="col-sm-2 col-form-label"
												>Subject</label
											>
											<div class="col-sm-10">
												<input
													type="text"
													readonly
													class="form-control-plaintext"
													id="periodChange"
													name="periodChange"
													value="${period}"
													hidden
												/>
												<select
													name="subjectChange"
													id="subjectChange"
													class="form-select"
													disabled
												>
                                                `;
                timetable.forEach(table => {
					if (table.period == period) {
						form += `
                        <option value="${table.period}" selected>
                            ${table.subj_name}
                        </option>
                        `;
					}
				});
				form += `
                </select>
                </div>
                </div>
                <div class="mb-3 row">
					<label for="statusChange" class="col-sm-2 col-form-label"
						>Status</label
					>
					<div class="col-sm-10">
						<select name="statusChange" id="statusChange" class="form-select">
                `;

				all_status.forEach(status => {
					if (status.status_key == val.status_key) {
						form += `
                        <option value="${status.status_key}" selected>
                            ${status.status_name}
                        </option>
                        `;
					} else {
						form += `
                        <option value="${status.status_key}">
                            ${status.status_name}
                        </option>
                        `;
					}
				});

				form += `
                </select>
				</div>
			    </div>
				</div>
                <div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						data-bs-dismiss="modal"
					>
						Close
					</button>
					<button type="submit" class="btn btn-primary">
						Save changes
					</button>
				</div>
				</form>
				</div>
				</div>
				</div>
                `;
                table.innerHTML += item;
				modalCon.innerHTML += form;
			});
		});
}