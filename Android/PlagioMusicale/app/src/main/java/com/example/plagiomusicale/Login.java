package com.example.plagiomusicale;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.Toast;

import com.fasterxml.jackson.databind.ObjectMapper;

import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class Login extends AppCompatActivity {

    private boolean doubleBackToExitPressedOnce;
    private EditText email;
    private EditText password;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        email=findViewById(R.id.emailTW);
        password=findViewById(R.id.passwordTW);
    }

    /*public void ResetPW(View view)
    {
        Intent resetPW = new Intent(Login.this,ResetPW.class);
        startActivity(resetPW);
    }*/
    public void VaiBack(View view){
        finish();
    }
    public void LoginActivity(View view){
        new LoginTask(this).execute(email.getText().toString(),password.getText().toString());
    }
    public void GuestLogin(View view){
        Intent guest = new Intent(this,Menu.class);
        startActivity(guest);
        finish();
    }

    public void About(View view){
        Intent about = new Intent(this,About.class);
        startActivity(about);
        finish();
    }
    @Override
    public void onBackPressed() {
        if (doubleBackToExitPressedOnce) {
            super.onBackPressed();
            return;
        }
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


class LoginTask extends AsyncTask<String,Integer,String> {

private Context context;

public LoginTask(Context context){
    this.context=context;
}
private boolean trovato;
    @Override
    protected String doInBackground(String... strings) {
        trovato=false;
        OkHttpClient client = new OkHttpClient();
        String url;
        if(strings.length==2)
        {
            url = "http://10.0.2.2:5000/loginMobile?mail="+strings[0]+"&pw="+strings[1];
        }
        else
            return null;
        System.out.println(url);
        Request request = new Request.Builder().url(url).build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                String esito = response.body().string();
                System.out.println("ESITO:"+esito);
                trovato=true;
            }
        });
        return strings[0];
    }

    @Override
    protected void onPostExecute(String string) {
        super.onPostExecute(string);
        while(!trovato){} //Aspettiamo la risposta dal server
        Intent login = new Intent(context, Menu.class);
        login.putExtra("mail",string); //Salviamo la mail dell'utente autenticato
        context.startActivity(login); //Reindirizziamo al Menu
        System.out.println("LOGIN COME: "+string);
    }

}