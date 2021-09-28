/*package com.example.plagiomusicale;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

import androidx.appcompat.app.AppCompatActivity;

import org.jetbrains.annotations.NotNull;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class ResetPW extends AppCompatActivity {
    private EditText email;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_reset_password);
        email=findViewById(R.id.emailTW);

    }
    public void VaiBack(View view){
        finish();
    }
    public void ResetPW(View view){
        new ResetTask(this).execute(email.getText().toString());
    }

    class ResetTask extends AsyncTask<String,Integer,String> {

        private Context context;

        public ResetTask(Context context) {
            this.context = context;
        }

        private boolean finito;

        @Override
        protected String doInBackground(String... strings) {
            finito = false;
            OkHttpClient client = new OkHttpClient();
            String url;
            if (strings.length == 1) {
                url = "http://10.0.2.2:5000/reset_passwordMobile?mail=" + strings[0];
            } else
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
                    finito = true;
                }
            });
            return strings[0];
        }

        @Override
        protected void onPostExecute(String string) {
            while (!finito) {
            }
            Intent main = new Intent(context, MainActivity.class);
            context.startActivity(main);
            super.onPostExecute(string);
            finish();
        }
    }
}
*/