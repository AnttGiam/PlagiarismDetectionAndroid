package com.example.plagiomusicale;

import android.os.Bundle;

import android.os.Handler;
import android.os.Looper;
import android.view.MenuItem;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.android.material.navigation.NavigationBarView;


public class Menu extends AppCompatActivity {

    private boolean doubleBackToExitPressedOnce;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Bundle datiUtente = new Bundle();
        String mailUser = getIntent().getStringExtra("mail");
        System.out.println("MAIL: "+mailUser);
        datiUtente.putString("mailUser",mailUser);
        if(mailUser!=null)
            setContentView(R.layout.activity_menu_logged);
        else
            setContentView(R.layout.activity_menu_guest);
        BottomNavigationView bNav = findViewById(R.id.menu);
        FragmentTransaction ft =  getSupportFragmentManager().beginTransaction();
        ft.setTransition(FragmentTransaction.TRANSIT_FRAGMENT_OPEN);
        Fragment fragment=new ViewCases();
        fragment.setArguments(datiUtente);
        ft.replace(R.id.fragment_container, fragment);
        ft.addToBackStack(null);
        ft.commit();
        bNav.setOnItemSelectedListener(new NavigationBarView.OnItemSelectedListener(){
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                Fragment fragment = null;
                switch (item.getItemId()){
                    case R.id.nav_check:
                    {
                        fragment=new UploadSong();
                        break;
                    }
                    case R.id.nav_profile:
                    {
                        fragment=new UserPage();
                        break;
                    }
                    case R.id.nav_new:
                    {
                        fragment=new NewCase();
                        break;
                    }
                    default:
                    {
                        fragment=new ViewCases();
                        break;
                    }
                }
                FragmentTransaction ft =  getSupportFragmentManager().beginTransaction();
                ft.setTransition(FragmentTransaction.TRANSIT_FRAGMENT_OPEN);
                fragment.setArguments(datiUtente);
                ft.replace(R.id.fragment_container, fragment);
                ft.addToBackStack(null);
                ft.commit();
                return true;
            }
        });
    }

    @Override
    public void onBackPressed() {
        if (doubleBackToExitPressedOnce) {
            super.onBackPressed();
            return;
        }
        getSupportFragmentManager().popBackStack();
        this.doubleBackToExitPressedOnce = true;
        Toast.makeText(this, "Premi di nuovo indietro per uscire", Toast.LENGTH_SHORT).show();

        new Handler(Looper.getMainLooper()).postDelayed(new Runnable() {

            @Override
            public void run() {
                doubleBackToExitPressedOnce=false;
            }
        }, 2000);
    }
}