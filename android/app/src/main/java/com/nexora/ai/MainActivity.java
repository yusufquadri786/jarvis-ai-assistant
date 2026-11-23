package com.nexora.ai;

import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.view.ViewGroup;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {
    private static final String PREFS = "nexora_settings";
    private static final String SERVER_URL = "server_url";
    private WebView webView;
    private EditText serverInput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        String configured = BuildConfig.BACKEND_URL.trim();
        SharedPreferences prefs = getSharedPreferences(PREFS, MODE_PRIVATE);
        String saved = prefs.getString(SERVER_URL, configured);
        if (saved != null && !saved.trim().isEmpty()) openAssistant(saved.trim());
        else showServerSetup();
    }

    private void showServerSetup() {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(24), dp(36), dp(24), dp(24));
        root.setBackgroundColor(Color.rgb(7, 14, 27));

        TextView title = new TextView(this);
        title.setText("NEXORA AI");
        title.setTextColor(Color.rgb(105, 190, 255));
        title.setTextSize(29);
        title.setPadding(0, 0, 0, dp(8));
        title.setTypeface(null, 1);
        root.addView(title);

        TextView info = new TextView(this);
        info.setText("Connect your secure NEXORA AI server to continue. Paste the HTTPS server address provided after backend deployment.");
        info.setTextColor(Color.LTGRAY);
        info.setTextSize(15);
        root.addView(info);

        serverInput = new EditText(this);
        serverInput.setSingleLine(true);
        serverInput.setTextColor(Color.WHITE);
        serverInput.setHintTextColor(Color.GRAY);
        serverInput.setHint("https://your-service.example.com");
        serverInput.setText(getSharedPreferences(PREFS, MODE_PRIVATE).getString(SERVER_URL, BuildConfig.BACKEND_URL));
        serverInput.setInputType(android.text.InputType.TYPE_CLASS_TEXT | android.text.InputType.TYPE_TEXT_VARIATION_URI);
        LinearLayout.LayoutParams inputParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        inputParams.topMargin = dp(24);
        root.addView(serverInput, inputParams);

        Button connect = new Button(this);
        connect.setText("Connect to NEXORA AI");
        LinearLayout.LayoutParams buttonParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        buttonParams.topMargin = dp(16);
        root.addView(connect, buttonParams);
        connect.setOnClickListener(v -> {
            String url = serverInput.getText().toString().trim();
            if (!isSecureServerUrl(url)) {
                Toast.makeText(this, "Enter a valid HTTPS server address.", Toast.LENGTH_LONG).show();
                return;
            }
            getSharedPreferences(PREFS, MODE_PRIVATE).edit().putString(SERVER_URL, url).apply();
            openAssistant(url);
        });

        TextView note = new TextView(this);
        note.setText("Your AI provider key stays on the server; it is never stored in this app.");
        note.setTextColor(Color.GRAY);
        note.setTextSize(12);
        LinearLayout.LayoutParams noteParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        noteParams.topMargin = dp(20);
        root.addView(note, noteParams);
        setContentView(root);
    }

    private boolean isSecureServerUrl(String value) {
        try {
            Uri uri = Uri.parse(value);
            return "https".equalsIgnoreCase(uri.getScheme())
                    && uri.getHost() != null && uri.getUserInfo() == null;
        } catch (Exception ignored) {
            return false;
        }
    }

    private void openAssistant(String url) {
        if (!isSecureServerUrl(url)) {
            showServerSetup();
            Toast.makeText(this, "A valid HTTPS server URL is required.", Toast.LENGTH_LONG).show();
            return;
        }
        Uri server = Uri.parse(url);
        webView = new WebView(this);
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        webView.setWebChromeClient(new WebChromeClient());
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri target = request.getUrl();
                return !("https".equalsIgnoreCase(target.getScheme())
                        && target.getHost() != null
                        && target.getHost().equalsIgnoreCase(server.getHost()));
            }
        });
        setContentView(webView);
        webView.loadUrl(url);
    }

    private int dp(int value) {
        return (int) (value * getResources().getDisplayMetrics().density + 0.5f);
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }
}
