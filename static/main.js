(function() {
    function showToast(message, type, backgrundColor) {
            var toastContainer = document.getElementById('toastContainer');
            var toastId = 'toast' + Date.now();

            // Create a new toast element
            var toastElement = document.createElement('div');
            toastElement.id = toastId;
            toastElement.className = 'toast';
            toastElement.setAttribute('role', 'alert');
            toastElement.setAttribute('aria-live', 'assertive');
            toastElement.setAttribute('aria-atomic', 'true');

            // Set the toast type if provided
            if (type && !backgroundColor) {
                toastElement.classList.add('toast-' + type);
            }

            // Set the custom background color if provided
            if (backgroundColor) {
                toastElement.style.backgroundColor = backgroundColor;
            }

            // Create the toast body
            var toastBody = document.createElement('div');
            toastBody.className = 'toast-body';
            toastBody.innerText = message;

            // Add close button to toast
            toastElement.appendChild(createCloseButton());
            toastElement.appendChild(toastBody); // Add the toast body to the toast element

            // Add the toast element to the container
            toastContainer.appendChild(toastElement);

            // Initialize the Bootstrap Toast
            var toast = new bootstrap.Toast(document.getElementById(toastId), {
                autohide: false // Prevents auto-hiding when close button is clicked
            });

            // Show the toast
            toast.show();

            // Remove the toast element after 10 seconds
            setTimeout(function () {
                toast.dispose();
                toastContainer.removeChild(toastElement);
            }, 10000);
        }

        function createCloseButton() {
            var closeButton = document.createElement('button');
            closeButton.type = 'button';
            closeButton.className = 'btn-close';
            closeButton.setAttribute('data-bs-dismiss', 'toast');
            closeButton.setAttribute('aria-label', 'Close');

            return closeButton;
        }

        window.showToast = showToast;

    function performOperation(operation) {
        console.log(`${operation} function called.`);
        var inputId = operation === 'encrypt' ? 'data' : 'encryptedData';
        var inputData = document.getElementById(inputId).value;
        var key = document.getElementById('key').value;

        if (!inputData || !key) {
            showToast(`${operation.charAt(0).toUpperCase() + operation.slice(1)}: Data and key are required.`);
            return;
        }

        fetch(`/${operation}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                [operation === 'encrypt' ? 'data' : 'encrypted_data']: inputData,
                'key': key,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`${operation.charAt(0).toUpperCase() + operation.slice(1)} failed. Please check your input.`);
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('result').value = data.result;
            resetCopyButton();
        })
        .catch(error => {
            showToast(`Error: ${error.message}`);
            console.error('Error:', error);
        });
    }

    function copyToClipboard() {
        var resultTextArea = document.getElementById('result');
        var result = resultTextArea.value.trim();

        if (result !== '') {
            resultTextArea.select();
            resultTextArea.setSelectionRange(0, result.length);

            document.execCommand('copy');

            resultTextArea.setSelectionRange(0, 0);

            var copyButton = document.getElementById('copyButton');
            copyButton.innerText = 'Copied';
            copyButton.classList.add('copied');
        }
    }

    function resetCopyButton() {
        var copyButton = document.getElementById('copyButton');
        copyButton.innerText = 'Copy';
        copyButton.classList.remove('copied');
    }
})();
