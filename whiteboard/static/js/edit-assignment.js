function initialize() {
    assignment_type = document.getElementById("assignmenttype");
    assignment_name = document.getElementById("assignmentName");
    numerator = document.getElementById("weight_numerator");
    denominator = document.getElementById("weight_denominator");
    calculated = document.getElementById("weight_calculated");
}

function takeSuggestion(newType, newName) {
    assignment_type.value = newType;
    assignment_name.value = newName;
}

function calculateWeight() {
    var weight = Number.parseInt(numerator.value) / Number.parseInt(denominator.value);
    calculated.innerHTML = weight.toFixed(2);
}
