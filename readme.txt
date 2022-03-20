.class public final Lcom/example/obfuscate_test/FirstFragment;
.super Landroidx/fragment/app/Fragment;
.source "FirstFragment.kt"


# annotations
.annotation runtime Lkotlin/Metadata;
    d1 = {
        "\u00004\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0008\u0002\n\u0002\u0018\u0002\n\u0002\u0008\u0004\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0002\u0008\u0003\u0018\u00002\u00020\u0001B\u0005\u00a2\u0006\u0002\u0010\u0002J&\u0010\u0008\u001a\u0004\u0018\u00010\t2\u0006\u0010\n\u001a\u00020\u000b2\u0008\u0010\u000c\u001a\u0004\u0018\u00010\r2\u0008\u0010\u000e\u001a\u0004\u0018\u00010\u000fH\u0016J\u0008\u0010\u0010\u001a\u00020\u0011H\u0016J\u001a\u0010\u0012\u001a\u00020\u00112\u0006\u0010\u0013\u001a\u00020\t2\u0008\u0010\u000e\u001a\u0004\u0018\u00010\u000fH\u0016R\u0010\u0010\u0003\u001a\u0004\u0018\u00010\u0004X\u0082\u000e\u00a2\u0006\u0002\n\u0000R\u0014\u0010\u0005\u001a\u00020\u00048BX\u0082\u0004\u00a2\u0006\u0006\u001a\u0004\u0008\u0006\u0010\u0007\u00a8\u0006\u0014"
    }
    d2 = {
        "Lcom/example/obfuscate_test/FirstFragment;",
        "Landroidx/fragment/app/Fragment;",
        "()V",
        "_binding",
        "Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;",
        "binding",
        "getBinding",
        "()Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;",
        "onCreateView",
        "Landroid/view/View;",
        "inflater",
        "Landroid/view/LayoutInflater;",
        "container",
        "Landroid/view/ViewGroup;",
        "savedInstanceState",
        "Landroid/os/Bundle;",
        "onDestroyView",
        "",
        "onViewCreated",
        "view",
        "app_release"
    }
    k = 0x1
    mv = {
        0x1,
        0x6,
        0x0
    }
    xi = 0x30
.end annotation


# instance fields
.field private _binding:Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;


# direct methods
.method public static synthetic $r8$lambda$sdjc5WGK8Nyl0tFlT7zb-jsiScw(Lcom/example/obfuscate_test/FirstFragment;Landroid/view/View;)V
    .locals 0

    invoke-static {p0, p1}, Lcom/example/obfuscate_test/FirstFragment;->onViewCreated$lambda-0(Lcom/example/obfuscate_test/FirstFragment;Landroid/view/View;)V

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .line 14
    invoke-direct {p0}, Landroidx/fragment/app/Fragment;-><init>()V

    return-void
.end method

.method private final getBinding()Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;
    .locals 1

    .line 20
    iget-object v0, p0, Lcom/example/obfuscate_test/FirstFragment;->_binding:Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;

    invoke-static {v0}, Lkotlin/jvm/internal/Intrinsics;->checkNotNull(Ljava/lang/Object;)V

    return-object v0
.end method

.method private static final onViewCreated$lambda-0(Lcom/example/obfuscate_test/FirstFragment;Landroid/view/View;)V
    .locals 0

    const-string p1, "this$0"

    invoke-static {p0, p1}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullParameter(Ljava/lang/Object;Ljava/lang/String;)V

    .line 36
    check-cast p0, Landroidx/fragment/app/Fragment;

    invoke-static {p0}, Landroidx/navigation/fragment/FragmentKt;->findNavController(Landroidx/fragment/app/Fragment;)Landroidx/navigation/NavController;

    move-result-object p0

    const p1, 0x7f080035

    invoke-virtual {p0, p1}, Landroidx/navigation/NavController;->navigate(I)V

    return-void
.end method


# virtual methods
.method public onCreateView(Landroid/view/LayoutInflater;Landroid/view/ViewGroup;Landroid/os/Bundle;)Landroid/view/View;
    .locals 0

    const-string p3, "inflater"

    invoke-static {p1, p3}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullParameter(Ljava/lang/Object;Ljava/lang/String;)V

    const/4 p3, 0x0

    .line 27
    invoke-static {p1, p2, p3}, Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;->inflate(Landroid/view/LayoutInflater;Landroid/view/ViewGroup;Z)Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;

    move-result-object p1

    iput-object p1, p0, Lcom/example/obfuscate_test/FirstFragment;->_binding:Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;

    .line 28
    invoke-direct {p0}, Lcom/example/obfuscate_test/FirstFragment;->getBinding()Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;

    move-result-object p1

    invoke-virtual {p1}, Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;->getRoot()Landroidx/constraintlayout/widget/ConstraintLayout;

    move-result-object p1

    check-cast p1, Landroid/view/View;

    return-object p1
.end method

.method public onDestroyView()V
    .locals 1

    .line 41
    invoke-super {p0}, Landroidx/fragment/app/Fragment;->onDestroyView()V

    const/4 v0, 0x0

    .line 42
    iput-object v0, p0, Lcom/example/obfuscate_test/FirstFragment;->_binding:Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;

    return-void
.end method

.method public onViewCreated(Landroid/view/View;Landroid/os/Bundle;)V
    .locals 1

    const-string v0, "view"

    invoke-static {p1, v0}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullParameter(Ljava/lang/Object;Ljava/lang/String;)V

    .line 33
    invoke-super {p0, p1, p2}, Landroidx/fragment/app/Fragment;->onViewCreated(Landroid/view/View;Landroid/os/Bundle;)V

    .line 35
    invoke-direct {p0}, Lcom/example/obfuscate_test/FirstFragment;->getBinding()Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;

    move-result-object p1

    iget-object p1, p1, Lcom/example/obfuscate_test/databinding/FragmentFirstBinding;->buttonFirst:Landroid/widget/Button;

    new-instance p2, Lcom/example/obfuscate_test/FirstFragment$$ExternalSyntheticLambda0;

    invoke-direct {p2, p0}, Lcom/example/obfuscate_test/FirstFragment$$ExternalSyntheticLambda0;-><init>(Lcom/example/obfuscate_test/FirstFragment;)V

    invoke-virtual {p1, p2}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    return-void
.end method
