document.addEventListener('DOMContentLoaded', function() {
    
    const form = document.querySelector('form');
    const input = document.getElementById('cv_upload');
    const label = document.querySelector('.custom-file-upload');
    const submitBtn = document.querySelector('.custom-file-upload'); 

   
    input.addEventListener('change', function(e) {
        if (this.files && this.files.length > 0) {
            const fileName = this.files[0].name;
            
            label.innerHTML = `📄 ${fileName} - Cliquez pour changer`;
            
            
          
            form.submit(); 
            
            
            label.innerHTML = "⏳ Analyse IA en cours...";
            label.style.opacity = "0.7";
            label.style.pointerEvents = "none";
        }
    });
});