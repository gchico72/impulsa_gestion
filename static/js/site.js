(function(){
  document.addEventListener('DOMContentLoaded', function(){
    var hamburger = document.getElementById('hamburger');
    var sidebar = document.getElementById('site-sidebar');
    if(!hamburger || !sidebar) return;

    function toggle(){
      var expanded = hamburger.getAttribute('aria-expanded') === 'true';
      hamburger.setAttribute('aria-expanded', String(!expanded));
      var hidden = sidebar.getAttribute('aria-hidden') === 'true';
      sidebar.setAttribute('aria-hidden', String(!hidden));
      sidebar.classList.toggle('sidebar-collapsed');
    }

    hamburger.addEventListener('click', function(e){
      e.preventDefault();
      toggle();
    });

    // Close sidebar when clicking outside on small screens
    document.addEventListener('click', function(e){
      var target = e.target;
      if(window.innerWidth > 700) return;
      if(!sidebar.classList.contains('sidebar-collapsed')) return;
      if(target === sidebar || sidebar.contains(target) || target === hamburger) return;
      // collapse
      sidebar.classList.add('sidebar-collapsed');
      sidebar.setAttribute('aria-hidden', 'true');
      hamburger.setAttribute('aria-expanded', 'false');
    });
  });
})();
